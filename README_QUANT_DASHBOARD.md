# Rayne Hedge Fund - Quant Dashboard (Excel + Google Sheets)

## 📊 What You Have

### Files Created

1. **Rayne_Hedge_Fund_Quant_Dashboard.xlsx** (Primary Workbook)
   - 4 professional sheets with formulas, formatting, and charts
   - Dark theme matching your HTML dashboard
   - 40+ metrics pre-calculated
   - Ready to import into Google Sheets

2. **GOOGLE_SHEETS_SETUP_GUIDE.md** (Detailed Instructions)
   - Step-by-step setup for each sheet
   - Formula templates you can copy/paste
   - Color scheme specifications
   - Data import instructions

3. **README.md** (This file)

---

## 🚀 Quick Start

### In Excel
1. Open `Rayne_Hedge_Fund_Quant_Dashboard.xlsx`
2. Review the 4 sheets (tabs at bottom)
3. Replace sample data with your actual trade data
4. All formulas auto-calculate

### In Google Sheets (Fastest)
1. Open Google Drive → Create → Google Sheets
2. File → Import spreadsheet → Upload the .xlsx file
3. Done! All formatting and formulas transfer

### Or: Manual Google Sheets Setup (Most Control)
1. Follow the detailed instructions in `GOOGLE_SHEETS_SETUP_GUIDE.md`
2. Copy/paste section by section
3. Takes ~30 minutes for full setup

---

## 📋 Sheet-by-Sheet Overview

### Sheet 1: BACKTEST LAB
**Purpose:** Test strategies across different Risk:Reward ratios with comprehensive metrics

**Key Sections:**
- Strategy selector dropdown
- RR Summary Table (5-RR levels)
  - Trades, Wins, Losses, Win %
  - Profit Factor, Expectancy, Total R, Max DD
- Key Metrics panel (CAGR, Sharpe, Sortino, max DD, win rate, profit factor)
- Equity curve chart (strategy vs buy & hold)
- Win/Loss distribution pie chart

**Pre-Built Formulas:**
- Win/Loss counts from trade log
- Profit factor calculation
- Expectancy derivation
- Drawdown tracking

**Action Items:**
- Upload your trade data to "TradeLog" sheet
- Formulas auto-reference and recalculate

---

### Sheet 2: VALIDATION SUITE
**Purpose:** Institutional-grade statistical validation (Monte Carlo, Bootstrap, PSR)

**Key Sections:**
- Validation Report Card (4-point checklist)
  - Permutation test p-value
  - Probabilistic Sharpe Ratio (PSR)
  - Bootstrap CI width
  - Robustness to slippage
- Bootstrap Confidence Intervals table
  - 95% CI for expectancy, win rate, profit factor, max DD
  - Precision calculation
- Permutation test histogram
  - Visual representation of edge significance

**Color Coding:**
- Green: PASS (edge is real, p < 0.05)
- Amber: WARNING (marginal, 0.05 < p < 0.10)
- Red: FAIL (no edge detected)

**Pre-Built Formulas:**
- CI width = ABS(CI_HIGH - CI_LOW) / ESTIMATE
- Precision = CI_WIDTH / ESTIMATE (as percentage)

**Action Items:**
- Plug in your permutation test results from Python/C++
- Bootstrap iterations auto-calculate from trade log

---

### Sheet 3: GOVERNANCE
**Purpose:** Strategy lifecycle tracking, pre-registration, and live trade decay monitoring

**Key Sections:**
- Lifecycle stages (Idea → Hypothesis → Validation → Paper → Live)
- Pre-registered acceptance criteria (locked before validation)
  - Min expectancy, sample size, max DD, min profit factor, min PSR
- Decision log (append-only audit trail)
  - Date, decision type, signer, rationale
- Live trade tracker
  - Real-time cumulative R vs backtest envelope

**Key Workflows:**
1. Set criteria in "Pre-registered Criteria" section
2. Record all promotions/demotions in Decision Log
3. Add live trades daily in Live Trade Tracker
4. Chart shows if live performance is within 95% confidence band

**Pre-Built Formulas:**
- Cumulative R calculation
- Upper/lower envelope bounds (±1.96σ from backtest expectancy)

**Action Items:**
- Update Decision Log when you promote/demote a strategy
- Add live trades as they execute
- Chart auto-updates

---

### Sheet 4: PORTFOLIO ALLOCATOR
**Purpose:** Multi-strategy portfolio construction with correlation-adjusted risk

**Key Sections:**
- Strategy Roster (all live/paper strategies with their metrics)
  - Status, CAGR, Sharpe, Max DD, Weight %, Allocation $
- Correlation Matrix (editable)
  - Click any cell to update correlation
  - Color-coded (high correlation = bright blue warning)
- Portfolio Summary metrics
  - Blended CAGR, Sharpe, Max DD
  - Diversification ratio
- Risk–Return map (efficient frontier scatter plot)
  - Each strategy + portfolio aggregate
- Allocation pie chart

**Allocation Methods (in dropdown):**
- Equal Weight (1/N)
- Risk Parity (1/σ)
- Max Sharpe proxy
- Inverse Drawdown
- Manual (you set weights)

**Pre-Built Formulas:**
- Portfolio Sharpe = (Σ w_i × Sharpe_i) adjusted for correlation
- Portfolio Max DD approximation
- Diversification Ratio = Σ w_i × σ_i / σ_portfolio

**Action Items:**
- Populate Strategy Roster (should auto-pull from Governance tab)
- Review/adjust correlation matrix (default: sector/asset-class correlations)
- Run "Build Portfolio" to generate charts

---

## 🎨 Design Features

### Color Scheme (Professional Dark Theme)
```
Background:        #0F1419 (Dark Navy)
Panel:            #161B22 (Slightly lighter)
Panel 2:          #1C2230 (Even lighter)
Border:           #2A3140 (Subtle border)
Text:             #E6EDF3 (Light gray)
Muted:            #8B95A7 (Muted text)

Accent:           #4F8CFF (Blue)
Success:          #26D07C (Green) — for wins, passes
Danger:           #EF4F56 (Red) — for losses, failures
Warning:          #F5B740 (Amber) — for caution/pending
Info:             #A37BF2 (Purple) — for information
```

### Typography
- Headers: Bold, 10–11px, muted color
- Values: 11–14px, light color
- Metrics: Bold, green (positive) or red (negative)
- Monospace data: Tabular-nums for alignment

### Charts
All charts include:
- Dark background
- Colored series (green for strategy, red for drawdown)
- Professional legend
- Axis labels
- Data labels on key points

---

## 📊 Metrics Explained

### From Backtest Lab
| Metric | Meaning | Target |
|--------|---------|--------|
| Win Rate | % of trades that profit | >50% |
| Profit Factor | Total wins / Total losses | >1.5 |
| Expectancy | Expected R per trade | >0.25 |
| Max Drawdown | Worst peak-to-trough | <20% |
| Sharpe Ratio | Return per unit of risk | >1.0 |

### From Validation Suite
| Test | Meaning | Pass Threshold |
|------|---------|----------------|
| Permutation p-value | Is edge better than luck? | <0.05 |
| PSR (Prob. Sharpe) | Confidence in positive Sharpe | >0.80 |
| Bootstrap CI | Precision of estimates | Width <50% of estimate |
| Robustness | Does edge survive slippage? | >0.8x at 2-tick buffer |

### From Governance
| Metric | Meaning |
|--------|---------|
| Lifecycle Stage | Strategy maturity (Idea→Live) |
| Pre-reg Criteria | Thresholds set before validation |
| Decision Log | Permanent audit trail |
| Live Trade Envelope | 95% CI band around backtest |

### From Portfolio
| Metric | Meaning |
|--------|---------|
| Correlation | Co-movement of strategies (−1 to +1) |
| Diversification Ratio | Benefit of combining strategies |
| Efficient Frontier | All possible risk/return combinations |

---

## 🔧 How to Customize

### Replace Sample Data

#### Step 1: Create "TradeLog" Sheet
1. New sheet → name it "TradeLog"
2. Add columns: `Date, Entry, Exit, RiskAmt, RewardAmt, Outcome, RR`
3. Paste your trade data (CSV import)

#### Step 2: Update Formulas
In Backtest Lab, update row 7 formula:
```
Before: =COUNTIFS(TradeLog!$C:$C,"Win")
After:  =COUNTIFS(TradeLog!$G:$G,"Win")
```

#### Step 3: Refresh Charts
Charts auto-update when data changes

### Add Your Strategies to Governance
1. Go to Governance sheet
2. Add new rows to Strategy Roster
3. Fill in CAGR, Sharpe, Max DD from your backtests
4. These auto-flow to Portfolio Allocator

### Upload to Google Sheets
1. Open Google Drive
2. Upload the .xlsx file
3. Google Sheets auto-converts all formulas
4. Share link with your team

---

## 📈 Advanced Usage

### Monte Carlo Forecasting
For 1000-path Monte Carlo in Forecast section:
- Use `=NORMINV(RAND(), mean, std_dev)`
- Mean = backtest expectancy
- Std Dev = backtest trade return std dev
- Run for 252 days (1 year)

### Walk-Forward Optimization
To add walk-forward analysis:
1. Create new sheet "WalkForward"
2. Split data into rolling train/test windows
3. Track optimal parameters per window
4. Plot OOS vs IS expectancy gap

### Real-Time Live Tracking
1. Set up daily data import
   - Use Google Forms → auto-populate TradeLog
   - Or: IMPORTRANGE() from broker feed
2. Governance sheet auto-updates live envelope
3. Alerts when cumulative R < lower band

---

## 💾 File Versions

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | May 18, 2026 | Initial quant-level release (4 sheets, 40+ metrics) |

---

## 🤝 Support

### Formula Issues?
- All formulas use relative references (they adapt when you copy/paste)
- Check that TradeLog sheet exists and is named correctly
- Use `Ctrl+Shift+F9` (Excel) or `Cmd+Shift+F9` (Mac) to force recalc

### Charting Issues in Google Sheets?
- Charts sometimes need manual refresh
- Right-click chart → Edit chart → Data range
- Ensure your data range includes headers

### Need Different Metrics?
- Duplicate a metric row
- Change the formula
- Recolor as needed

---

## 📚 Related Files
- `GOOGLE_SHEETS_SETUP_GUIDE.md` — Detailed sheet-by-sheet instructions
- `Rayne_Hedge_Fund_Quant_Dashboard.xlsx` — The main workbook
- `Rayne Hedge Fund.html` — Original HTML dashboard (reference)

---

## ✅ Checklist: Getting Started

- [ ] Open `Rayne_Hedge_Fund_Quant_Dashboard.xlsx` in Excel or Google Sheets
- [ ] Review the 4 sheets and sample data
- [ ] Create "TradeLog" sheet with your actual trade data
- [ ] Update formulas to reference your TradeLog
- [ ] Verify charts update with your data
- [ ] Customize strategy names in Governance sheet
- [ ] Share with your team (Google Sheets recommended for collaboration)
- [ ] Set up daily live trade imports
- [ ] Schedule weekly review of Governance decision log

---

**Status:** Production-ready for Quant Analysts  
**Theme:** Professional dark mode (all metrics color-coded)  
**Scope:** Backtest analysis, validation, governance, portfolio optimization  
**Support:** All formulas template-based and easily customizable

---

*Created: May 18, 2026*  
*For: Rayne Hedge Fund - Senior Quantitative Analyst*  
*Quality:** Enterprise-grade analysis dashboard*
