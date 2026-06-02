# ─────────────────────────────────────────────────────────────────────────────
# Rayne Asset Management — Previous IB Order Block / Breaker Block
# QuantConnect Lean (Python) — Paper Trading
#
# Strategy (matches Rayne Hedge Fund.html IBOB engine exactly):
#
#   Block construction
#     Each day one block is created from the PREVIOUS day's IB range
#     (IB high / IB low).  Direction is set by where the previous day's
#     LAST CLOSE sits relative to the IB midpoint:
#       last_close >= midpoint  →  Bullish OB   (expect price to support)
#       last_close <  midpoint  →  Bearish OB   (expect price to resist)
#
#   Invalidation → Breaker Block
#     Bull OB  : bar LOW  pierces BELOW block bottom  → flips to Bear BB
#     Bear OB  : bar HIGH pierces ABOVE block top     → flips to Bull BB
#     (intrabar pierce, checked before entry on the same bar)
#
#   Entry trigger
#     Bull (OB or BB) : bar low  <= entry price   (price dips into block)
#     Bear (OB or BB) : bar high >= entry price   (price rallies into block)
#
#   Levels
#     Entry  : 50 % into the block from the near edge  (midpoint)
#     Stop   : 100 % of the block height               (far edge)
#     Target : 1 : 3 Risk-Reward
# ─────────────────────────────────────────────────────────────────────────────
from AlgorithmImports import *
from datetime import time as tradeTime, datetime, timedelta


class PrevIBOrderBreakerBlock(QCAlgorithm):

    # ── Strategy constants — edit these to tune ───────────────────────────────
    FUTURE_TICKER = "MES"              # Micro E-mini S&P 500 (CME)
    MULTIPLIER    = 5                  # MES = $5 per point  (ES = 50, MNQ = 2)
    IB_MINUTES    = 60                 # Initial Balance window (minutes from open)
    ENTRY_PCT     = 0.50               # Enter 50 % into block from the near edge
    STOP_PCT      = 1.00               # Stop at 100 % (opposite edge of block)
    RR            = 3.0                # Reward : Risk
    RISK_PCT      = 0.01               # Fraction of equity risked per trade (1 %)
    SESSION_OPEN  = tradeTime(9, 30)
    SESSION_CLOSE = tradeTime(15, 55)  # flatten 5 min before close
    # ─────────────────────────────────────────────────────────────────────────

    def initialize(self) -> None:
        self.set_start_date(2024, 1, 1)
        self.set_cash(25_000)          # typical MES account minimum
        self.set_brokerage_model(
            BrokerageName.INTERACTIVE_BROKERS_BROKERAGE, AccountType.MARGIN
        )

        mes = self.add_future(
            self.FUTURE_TICKER,
            resolution=Resolution.MINUTE,
            market=Market.CME,
            extended_market_hours=False,
        )
        mes.set_filter(timedelta(0), timedelta(90))   # front-month only
        self._canonical = mes.symbol                  # continuous symbol
        self._sym: Symbol | None = None               # resolved front-month contract

        # IB end time computed once from constants
        base = datetime(2000, 1, 1, self.SESSION_OPEN.hour, self.SESSION_OPEN.minute)
        self._ib_end: tradeTime = (base + timedelta(minutes=self.IB_MINUTES)).time()

        # ── Previous day's IB data (used to build today's block) ─────────────
        self._prev_ib_high:   float | None = None
        self._prev_ib_low:    float | None = None
        self._prev_day_lc:    float | None = None   # last close of previous day

        # ── Today's IB accumulators ───────────────────────────────────────────
        self._ib_high:        float | None = None
        self._ib_low:         float | None = None
        self._ib_done:        bool         = False
        self._day_last_close: float | None = None   # updated every bar

        # ── Active blocks (at most one OB + one BB per session) ──────────────
        self._ob: dict | None = None   # order block from prev-day IB
        self._bb: dict | None = None   # breaker block spawned when OB is pierced

        # ── Active trade state ────────────────────────────────────────────────
        self._entry_id:       int | None = None
        self._stop_id:        int | None = None
        self._target_id:      int | None = None
        self._pending_stop:   float      = 0.0
        self._pending_target: float      = 0.0
        self._pending_qty:    int        = 0
        self._pending_dir:    int        = 0

        # Daily events
        self.schedule.on(
            self.date_rules.every_day(),
            self.time_rules.at(9, 29),
            self._on_session_open,
        )
        self.schedule.on(
            self.date_rules.every_day(),
            self.time_rules.at(15, 55),
            self._on_session_close,
        )

    # ── Daily lifecycle ───────────────────────────────────────────────────────

    def _on_session_open(self) -> None:
        """
        Roll yesterday's IB range into today's block candidate, then reset
        accumulators for the new session.
        """
        # Build one block from the previous day's IB + last close
        if (self._prev_ib_high is not None
                and self._prev_ib_low is not None
                and self._prev_day_lc is not None):
            mid  = (self._prev_ib_high + self._prev_ib_low) / 2
            kind = "bull" if self._prev_day_lc >= mid else "bear"
            self._ob = {
                "kind": kind,
                "top":  self._prev_ib_high,
                "bot":  self._prev_ib_low,
                "used": False,
                "dead": False,
            }
            self.debug(
                f"{self.time.date()} | block: {kind.upper()} OB  "
                f"{self._prev_ib_low:.2f}–{self._prev_ib_high:.2f}  "
                f"(prev lc={self._prev_day_lc:.2f}  mid={mid:.2f})"
            )
        else:
            self._ob = None

        self._bb = None  # breaker block resets each session

        # Save current-day IB for use tomorrow (before resetting)
        self._prev_ib_high = self._ib_high
        self._prev_ib_low  = self._ib_low
        self._prev_day_lc  = self._day_last_close

        # Reset today's IB state
        self._ib_high        = None
        self._ib_low         = None
        self._ib_done        = False
        self._day_last_close = None

    def _on_session_close(self) -> None:
        if self.portfolio.invested:
            self.liquidate(tag="EOD")
            self._clear_trade_state()

    # ── Main data loop ────────────────────────────────────────────────────────

    def on_data(self, data: Slice) -> None:
        # Resolve front-month contract
        chain = data.future_chains.get(self._canonical)
        if chain is None:
            return
        contract = sorted(chain, key=lambda c: c.expiry)[0]
        self._sym = contract.symbol

        if not data.bars.contains_key(self._sym):
            return

        bar = data.bars[self._sym]
        now = self.time.time()

        # Always track the last close for the current day
        self._day_last_close = bar.close

        # 1. Accumulate IB range during the IB window; mark done when it closes
        if not self._ib_done:
            if self.SESSION_OPEN <= now <= self._ib_end:
                self._ib_high = max(self._ib_high or 0,   bar.high)
                self._ib_low  = min(self._ib_low  or 1e9, bar.low)
            elif self._ib_high is not None and now > self._ib_end:
                self._ib_done = True
                self.debug(
                    f"IB finalised {self._ib_high:.2f}/{self._ib_low:.2f}"
                )

        # Only trade after today's IB is established
        if not self._ib_done:
            return

        # 2. Check invalidations FIRST (same-bar order as HTML engine)
        self._update_breaker_blocks(bar)

        # 3. Seek entry if flat
        if (self._entry_id is None
                and not self.portfolio.invested
                and self.SESSION_OPEN < now < self.SESSION_CLOSE):
            self._seek_entry(bar)

    # ── Breaker Block promotion ───────────────────────────────────────────────

    def _update_breaker_blocks(self, bar: TradeBar) -> None:
        """
        Mirrors HTML invalidation logic exactly:
          Bull OB : bar low  < block bottom  → dead; spawn Bear BB
          Bear OB : bar high > block top     → dead; spawn Bull BB
        Uses intrabar pierce (low/high), not close.
        """
        ob = self._ob
        if ob is None or ob["dead"] or ob["used"]:
            return

        if ob["kind"] == "bull" and bar.low < ob["bot"]:
            ob["dead"] = True
            self._bb = {
                "kind": "bear", "top": ob["top"], "bot": ob["bot"],
                "used": False, "dead": False,
            }
            self.debug(f"Bull OB pierced → Bear BB  {ob['bot']:.2f}–{ob['top']:.2f}")

        elif ob["kind"] == "bear" and bar.high > ob["top"]:
            ob["dead"] = True
            self._bb = {
                "kind": "bull", "top": ob["top"], "bot": ob["bot"],
                "used": False, "dead": False,
            }
            self.debug(f"Bear OB pierced → Bull BB  {ob['bot']:.2f}–{ob['top']:.2f}")

    # ── Entry logic ───────────────────────────────────────────────────────────

    def _seek_entry(self, bar: TradeBar) -> None:
        """
        Entry trigger mirrors the HTML engine:
          Bull block : bar low  <= entry  (price dips into block)
          Bear block : bar high >= entry  (price rallies into block)

        Levels (identical to HTML):
          bull entry = top − height × ENTRY_PCT   (50 % → midpoint)
          bull stop  = top − height × STOP_PCT    (100 % → block low)
          bear entry = bot + height × ENTRY_PCT
          bear stop  = bot + height × STOP_PCT    (100 % → block high)

        Sizing accounts for MES point multiplier:
          qty = (equity × RISK_PCT) / (risk_points × MULTIPLIER)
        """
        candidates: list[dict] = []
        if self._ob and not self._ob["dead"] and not self._ob["used"]:
            candidates.append(self._ob)
        if self._bb and not self._bb["dead"] and not self._bb["used"]:
            candidates.append(self._bb)

        for block in candidates:
            bullish = block["kind"] == "bull"
            top, bot = block["top"], block["bot"]
            h = top - bot
            if h <= 0:
                continue

            if bullish:
                entry = top - h * self.ENTRY_PCT
                stop  = top - h * self.STOP_PCT
                if entry <= stop:
                    continue
                triggered = bar.low <= entry
            else:
                entry = bot + h * self.ENTRY_PCT
                stop  = bot + h * self.STOP_PCT
                if entry >= stop:
                    continue
                triggered = bar.high >= entry

            if not triggered:
                continue

            risk_points = abs(entry - stop)
            if risk_points <= 0:
                continue

            target    = entry + (1 if bullish else -1) * risk_points * self.RR
            direction = 1 if bullish else -1

            # Dollar risk ÷ (points × $/point) = contracts
            qty = max(1, int(
                self.portfolio.total_portfolio_value
                * self.RISK_PCT
                / (risk_points * self.MULTIPLIER)
            ))

            self.log(
                f"{'LONG' if bullish else 'SHORT'} "
                f"{'OB' if block is self._ob else 'BB'} | "
                f"block {bot:.2f}–{top:.2f} | "
                f"entry {entry:.2f}  stop {stop:.2f}  "
                f"target {target:.2f}  qty {qty} MES"
            )

            ticket = self.market_order(self._sym, direction * qty)
            self._entry_id       = ticket.order_id
            self._pending_stop   = stop
            self._pending_target = target
            self._pending_qty    = qty
            self._pending_dir    = direction
            block["used"]        = True
            break  # one position at a time

    # ── Order events — bracket wiring ─────────────────────────────────────────

    def on_order_event(self, order_event: OrderEvent) -> None:
        if order_event.status != OrderStatus.FILLED:
            return

        oid = order_event.order_id
        d, qty = self._pending_dir, self._pending_qty

        if oid == self._entry_id:
            sl = self.stop_market_order(
                self._sym, -d * qty, self._pending_stop, tag="SL"
            )
            tp = self.limit_order(
                self._sym, -d * qty, self._pending_target, tag="TP"
            )
            self._stop_id   = sl.order_id
            self._target_id = tp.order_id
            self._entry_id  = None

        elif oid == self._stop_id:
            self._cancel_safe(self._target_id)
            self.log(f"STOPPED OUT  {order_event.fill_price:.2f}")
            self._clear_trade_state()

        elif oid == self._target_id:
            self._cancel_safe(self._stop_id)
            self.log(f"TARGET HIT   {order_event.fill_price:.2f}")
            self._clear_trade_state()

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _cancel_safe(self, order_id: int | None) -> None:
        if order_id is None:
            return
        try:
            self.transactions.cancel_order(order_id)
        except Exception as e:
            self.debug(f"cancel {order_id} failed: {e}")

    def _clear_trade_state(self) -> None:
        self._entry_id       = None
        self._stop_id        = None
        self._target_id      = None
        self._pending_stop   = 0.0
        self._pending_target = 0.0
        self._pending_qty    = 0
        self._pending_dir    = 0


# ─────────────────────────────────────────────────────────────────────────────
# NOTES
# ─────────────────────────────────────────────────────────────────────────────
#
# 1. PAPER TRADING ON QUANTCONNECT
#    Create a new project, paste this file as main.py, then click
#    "Deploy Live" → select "Paper Trading (QuantConnect)" as the brokerage.
#    No live capital is at risk.
#
# 2. SWITCHING INSTRUMENTS
#    Change FUTURE_TICKER and MULTIPLIER at the top of the class:
#
#      Instrument   FUTURE_TICKER   MULTIPLIER
#      ──────────   ─────────────   ──────────
#      MES          "MES"           5          ← default
#      ES           "ES"            50
#      MNQ          "MNQ"           2
#      NQ           "NQ"            20
#      M2K (MRussell) "M2K"         5
#
# 3. PARAMETERS TO TUNE
#    IB_MINUTES  — 30 or 60 are common; 60 is the ICT standard
#    ENTRY_PCT   — 0.0 enters at the block edge; 0.5 enters at the midpoint
#    RISK_PCT    — 0.005 (0.5 %) for conservative sizing
#
# 4. WHAT THE ALGORITHM DOES NOT DO (intentional)
#    - requireMatch / session bias filter (HTML option to restrict to
#      bull-only or bear-only based on session open vs close)
#    - side filter (HTML: bullish / bearish / both)
#    - fillBuffer (HTML: tick offset before triggering entry)
#    - Multi-session OB carry-forward (prev day only)
#    - Partial take-profit
#    These are easy to add once you've validated the core logic.
# ─────────────────────────────────────────────────────────────────────────────
