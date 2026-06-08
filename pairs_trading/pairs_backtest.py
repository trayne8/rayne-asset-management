"""Pairs trading backtester example

This script performs:
1. Data fetch (yfinance)
2. Data munging and train/test split
3. Exploratory scatter matrix and correlation checks
4. Cointegration / OLS hedge ratio fitting on train set
5. Regression metrics: RMSE, adjusted R2, Durbin-Watson
6. Signal generation based on z-score of spread
7. Vectorized strategy P&L & performance (Sharpe, MaxDD) on train and test
8. Simple Backtrader demo that executes generated signals

Run: python pairs_trading/pairs_backtest.py
"""

import warnings
warnings.filterwarnings("ignore")

import os
from datetime import datetime

import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns

import statsmodels.api as sm
from statsmodels.tsa.stattools import coint
from statsmodels.stats.stattools import durbin_watson

import backtrader as bt


def fetch_data(tickers, start=None, end=None):
    df = yf.download(tickers, start=start, end=end, progress=False)
    if isinstance(tickers, (list, tuple)):
        close = df["Close"].copy()
        # preserve the requested ticker order, since yfinance may reorder columns
        close = close.loc[:, tickers]
    else:
        close = df["Close"].to_frame()
    close = close.dropna()
    close.index = pd.to_datetime(close.index)
    return close


def train_test_split(df, train_size=0.7):
    n = len(df)
    split = int(n * train_size)
    train = df.iloc[:split].copy()
    test = df.iloc[split:].copy()
    return train, test


def fit_hedge_ratio(y, x):
    x = sm.add_constant(x)
    model = sm.OLS(y, x).fit()
    # hedge ratio is coefficient of x
    beta = float(model.params[1])
    return model, beta


def regression_metrics(model, y, x):
    preds = model.predict(sm.add_constant(x))
    resid = y - preds
    rmse = float(np.sqrt(np.mean(resid ** 2)))
    adj_r2 = float(model.rsquared_adj)
    dw = float(durbin_watson(resid))
    return {"RMSE": rmse, "Adj_R2": adj_r2, "DurbinWatson": dw}


def zscore(series):
    return (series - series.mean()) / series.std()


def generate_signals(df, beta, lookback_mean=60, lookback_std=60, enter_z=2.0, exit_z=0.5):
    # spread = SP - beta * other
    spread = df.iloc[:, 0] - beta * df.iloc[:, 1]
    roll_mean = spread.rolling(lookback_mean).mean()
    roll_std = spread.rolling(lookback_std).std()
    z = (spread - roll_mean) / roll_std

    sig = pd.Series(0, index=df.index)
    # long spread when z < -enter_z  (buy spread => long first, short second)
    sig[z < -enter_z] = 1
    # short spread when z > enter_z
    sig[z > enter_z] = -1
    # exit when |z| < exit_z
    sig[np.abs(z) < exit_z] = 0

    # forward-fill positions: hold until exit signal
    pos = sig.replace(0, np.nan).ffill().fillna(0).astype(int)

    return pd.DataFrame({"spread": spread, "z": z, "signal_raw": sig, "position": pos})


def compute_strategy_returns(df, beta, positions, cost_rate=0.0, slippage_per_share=0.0):
    px = df.copy()
    px_ret = px.diff()
    pos_sp = positions
    pos_other = -beta * positions
    # basic PnL from price changes
    pnl = pos_sp.shift(1) * px_ret.iloc[:, 0] + pos_other.shift(1) * px_ret.iloc[:, 1]
    pnl = pnl.fillna(0)

    # transaction costs and slippage (approximate): based on change in position * price
    trades_sp = pos_sp.diff().abs().fillna(0)
    trades_other = pos_other.diff().abs().fillna(0)
    trade_value = trades_sp * px.iloc[:, 0] + trades_other * px.iloc[:, 1]
    cost = trade_value * cost_rate
    slippage_cost = (trades_sp + trades_other) * slippage_per_share

    total_cost = cost + slippage_cost

    # normalize by initial notional (use first day's close of SP)
    initial_notional = float(px.iloc[0, 0])
    strategy_ret = (pnl - total_cost) / initial_notional
    cumret = (1 + strategy_ret).cumprod() - 1
    return strategy_ret, cumret


def sharpe_ratio(returns, period_per_year=252):
    ann_ret = returns.mean() * period_per_year
    ann_vol = returns.std() * np.sqrt(period_per_year)
    if ann_vol == 0:
        return np.nan
    return ann_ret / ann_vol


def max_drawdown(cumret):
    running_max = cumret.cummax()
    drawdown = (cumret - running_max) / running_max.replace(0, np.nan)
    min_dd = drawdown.min(skipna=True)
    return float(min_dd) if np.isfinite(min_dd) else np.nan


def backtrader_demo(df, signal_map, hedge_ratio):
    cerebro = bt.Cerebro(stdstats=False)
    cerebro.broker.setcash(100000.0)

    class PandasFeed(bt.feeds.PandasData):
        params = (('datetime', None),)

    # Backtrader expects OHLCV columns. Build simple OHLC from Close and zero volume.
    df0 = pd.DataFrame({
        'open': df.iloc[:, 0],
        'high': df.iloc[:, 0],
        'low': df.iloc[:, 0],
        'close': df.iloc[:, 0],
        'volume': 0,
    }, index=df.index)
    df1 = pd.DataFrame({
        'open': df.iloc[:, 1],
        'high': df.iloc[:, 1],
        'low': df.iloc[:, 1],
        'close': df.iloc[:, 1],
        'volume': 0,
    }, index=df.index)
    data0 = PandasFeed(dataname=df0)
    data1 = PandasFeed(dataname=df1)
    cerebro.adddata(data0)
    cerebro.adddata(data1)

    class SpreadStrategy(bt.Strategy):
        params = (('signal_map', {}), ('hedge_ratio', 1.0),)

        def __init__(self):
            self.dat0 = self.datas[0]
            self.dat1 = self.datas[1]

        def next(self):
            dt = self.datas[0].datetime.date(0)
            sig = self.p.signal_map.get(dt, 0)
            pos0 = self.getposition(self.dat0).size
            pos1 = self.getposition(self.dat1).size
            # defensive hedge_ratio
            try:
                hr = float(self.p.hedge_ratio)
                if not np.isfinite(hr) or hr <= 0:
                    hr = 1.0
            except Exception:
                hr = 1.0

            # close logic
            if sig == 0:
                if pos0 != 0:
                    self.close(data=self.dat0)
                if pos1 != 0:
                    self.close(data=self.dat1)
            elif sig == 1:
                if pos0 == 0 and pos1 == 0:
                    price0 = float(self.dat0.close[0])
                    cash = float(self.broker.getcash())
                    if np.isnan(price0) or price0 <= 0 or cash <= 0:
                        return
                    target_notional = max(cash * 0.1, price0)
                    size = int(target_notional // price0)
                    if size <= 0:
                        return
                    hedge_size = int(round(size * hr))
                    if hedge_size <= 0:
                        hedge_size = 1
                    self.buy(data=self.dat0, size=size)
                    self.sell(data=self.dat1, size=hedge_size)
            elif sig == -1:
                if pos0 == 0 and pos1 == 0:
                    price0 = float(self.dat0.close[0])
                    cash = float(self.broker.getcash())
                    if np.isnan(price0) or price0 <= 0 or cash <= 0:
                        return
                    target_notional = max(cash * 0.1, price0)
                    size = int(target_notional // price0)
                    if size <= 0:
                        return
                    hedge_size = int(round(size * hr))
                    if hedge_size <= 0:
                        hedge_size = 1
                    self.sell(data=self.dat0, size=size)
                    self.buy(data=self.dat1, size=hedge_size)

    cerebro.addstrategy(SpreadStrategy, signal_map=signal_map, hedge_ratio=hedge_ratio)
    start_val = cerebro.broker.getvalue()
    cerebro.run()
    end_val = cerebro.broker.getvalue()
    return start_val, end_val


def sensitivity_analysis(close, beta, positions, train_last_idx, cost_rates=(0.0, 0.0001, 0.0005, 0.001), slippages=(0.0, 0.01, 0.05)):
    rows = []
    for cost in cost_rates:
        for slip in slippages:
            ret, cum = compute_strategy_returns(close, beta, positions, cost_rate=cost, slippage_per_share=slip)
            train_mask = ret.index <= train_last_idx
            test_mask = ret.index > train_last_idx
            train_sh = sharpe_ratio(ret[train_mask])
            test_sh = sharpe_ratio(ret[test_mask])
            train_mdd = max_drawdown(cum[train_mask])
            test_mdd = max_drawdown(cum[test_mask])
            rows.append({
                'cost_rate': cost,
                'slippage_per_share': slip,
                'train_sharpe': train_sh,
                'test_sharpe': test_sh,
                'train_maxdd': train_mdd,
                'test_maxdd': test_mdd,
            })
    df = pd.DataFrame(rows)
    return df


def main():
    # Example tickers: S&P500 index (^GSPC) vs Nasdaq ETF (QQQ)
    tickers = ['^GSPC', 'QQQ']
    start = '2018-01-01'
    end = datetime.today().strftime('%Y-%m-%d')

    close = fetch_data(tickers, start=start, end=end)
    if close.shape[1] < 2:
        raise SystemExit('Need two tickers with close prices')

    # split
    train, test = train_test_split(close, train_size=0.7)

    # exploratory scatter matrix on train
    plot_dir = 'pairs_trading/plots'
    os.makedirs(plot_dir, exist_ok=True)
    sns.pairplot(train.pct_change().dropna())
    plt.suptitle('Scatter matrix (train returns)')
    plt.savefig(os.path.join(plot_dir, 'scatter_matrix_train.png'))
    plt.close()

    # find highest correlation to S&P500 among other assets
    base = train.columns[0]
    corrs = train.pct_change().corr().loc[base].drop(base).abs().sort_values(ascending=False)
    print('Correlations to {}:'.format(base))
    print(corrs)

    partner = corrs.index[0]
    print(f'Chosen partner ticker: {partner}')

    # cointegration test
    coint_t, pvalue, _ = coint(train[base], train[partner])
    print(f'Cointegration test p-value: {pvalue:.4f} (t={coint_t:.4f})')

    # fit hedge ratio on train
    model, beta = fit_hedge_ratio(train[base], train[partner])
    print(f'Hedge ratio (beta): {beta:.4f}')

    metrics = regression_metrics(model, train[base], train[partner])
    print('Regression metrics (train):', metrics)

    # generate signals on full dataset using train's parameters for rolling windows
    signals_df = generate_signals(close[[base, partner]], beta)

    # compute returns / performance vectorized
    strat_ret, strat_cum = compute_strategy_returns(close[[base, partner]], beta, signals_df['position'])

    # performance on train vs test
    train_mask = strat_ret.index <= train.index[-1]
    test_mask = strat_ret.index > train.index[-1]

    train_sharpe = sharpe_ratio(strat_ret[train_mask])
    test_sharpe = sharpe_ratio(strat_ret[test_mask])
    train_mdd = max_drawdown(strat_cum[train_mask])
    test_mdd = max_drawdown(strat_cum[test_mask])

    print('\nPerformance:')
    print(f'Train Sharpe: {train_sharpe:.4f}, MaxDD: {train_mdd:.4f}')
    print(f'Test  Sharpe: {test_sharpe:.4f}, MaxDD: {test_mdd:.4f}')

    # Backtrader demo (optional) - build a date->signal map
    sig_map = {d.date(): int(s) for d, s in zip(signals_df.index, signals_df['position'])}
    try:
        start_val, end_val = backtrader_demo(close[[base, partner]], sig_map, hedge_ratio=abs(beta))
        print(f'Backtrader start value: {start_val:.2f} end value: {end_val:.2f}')
    except Exception as e:
        print('Backtrader demo failed:', e)

    # save a quick performance plot
    plt.figure(figsize=(10, 6))
    strat_cum.plot()
    plt.title('Strategy cumulative return')
    plt.tight_layout()
    plt.savefig(os.path.join(plot_dir, 'strategy_cum_return.png'))
    plt.close()


if __name__ == '__main__':
    main()
