# Rayne Hedge Fund - Google Sheets Quant Dashboard Setup Guide

## Overview
This guide walks you through creating a professional quant-level trading analysis dashboard in Google Sheets that mirrors the Excel workbook and replicates the HTML functionality.

## Quick Start (2 minutes)

### Option A: Import Pre-Built Template (Fastest)
1. Go to **[Google Drive](https://drive.google.com)** → **Create** → **Google Sheets**
2. Go to **File** → **Import spreadsheet** → **Upload** → Select the **Rayne_Hedge_Fund_Quant_Dashboard.xlsx** file
3. Choose **Replace current sheet** or **Create new sheets**
4. Done! All formatting and formulas transfer over

### Option B: Manual Setup (Most Control)
Follow the sheet-by-sheet instructions below.

---

## Sheet 1: BACKTEST LAB

### Column Headers (Row 1)
- **A1-D1:** Strategy Input Section
- **K1-M1:** Equity Curve Data (for charting)

### Section 1: Strategy Selector (A3:B3)
```
A3: Strategy:
B3: [Dropdown] → Options: Prev IB Order/Breaker Block, ORB, 4 NY Opens
```

### Section 2: RR Summary Table (A5:I11)
Create a table with these columns:

| RR | Trades | Wins | Losses | Win % | Profit Factor | Expectancy (R) | Total R | Max DD (R) |
|----|--------|------|--------|-------|----------------|-----------------|---------|-----------|
| 1 | [Formula] | [Formula] | [Formula] | `=C7/B7` | `=(C7*3)/(D7*1)` | 0.28 | `=B7*G7` | 12.5 |
| 1.5 | [Formula] | [Formula] | [Formula] | [Formula] | [Formula] | 0.32 | [Formula] | 12.8 |
| 2 | [Formula] | [Formula] | [Formula] | [Formula] | [Formula] | 0.35 | [Formula] | 13.1 |
| 3 | [Formula] | [Formula] | [Formula] | [Formula] | [Formula] | 0.38 | [Formula] | 13.5 |
| 4 | [Formula] | [Formula] | [Formula] | [Formula] | [Formula] | 0.41 | [Formula] | 14.0 |

**Key Formulas:**
- **Wins:** `=COUNTIFS(TradeLog!$C:$C,"Win")`
- **Losses:** `=COUNTIFS(TradeLog!$C:$C,"Loss")`
- **Win %:** `=C{row}/B{row}`
- **Profit Factor:** `=(C{row}*AVERAGE_WIN)/(D{row}*AVERAGE_LOSS)`
- **Expectancy:** `=(C{row}/B{row})*AVG_WINNER - (D{row}/B{row})*AVG_LOSER`

### Section 3: Key Metrics (A13:B19)
```
A13: Total Return %           B13: 47.2
A14: CAGR %                   B14: 22.3
A15: Sharpe Ratio             B15: 1.45
A16: Max Drawdown %           B16: 12.6
A17: Win Rate %               B17: 41.0
A18: Profit Factor            B18: 1.62
```

**Format:** B cells should be **green bold** (for positive values)

### Section 4: Equity Curve Data (K2:M51)
Create 50-row dataset:
```
K2: Period        L2: Cumulative R   M2: Buy & Hold
K3: 1            L3: 0.45           M3: 1.02
K4: 2            L4: 1.18           M4: 1.03
...
```

### Charts to Add
1. **Line Chart:** Equity Curve (K2:M51) → Place at A26
2. **Pie Chart:** Win/Loss Distribution → Place at K26

---

## Sheet 2: VALIDATION SUITE

### Section 1: Validation Report Card (A3:C7)
| Metric | Value | Status |
|--------|-------|--------|
| Permutation p-value | 0.032 | ✓ PASS (green) |
| Probabilistic Sharpe Ratio | 0.87 | ✓ PASS (green) |
| Bootstrap CI Width | ±0.18 | ⚠ ACCEPTABLE (amber) |
| Robustness (0 vs 2-tick) | 0.94x | ⚠ WARNING (amber) |

**Color Coding:**
- **PASS:** Green background (#26D07C), black text
- **WARNING:** Amber background (#F5B740), black text

### Section 2: Bootstrap CI Table (A10:E15)
```
A10: BOOTSTRAP CONFIDENCE INTERVALS (95%)

Headers: Metric | Estimate | 95% CI Low | 95% CI High | Precision

Rows:
Expectancy (R)        | 0.28 | 0.18 | 0.38 | =ABS(D{row}-C{row})/B{row}
Win Rate %            | 0.41 | 0.35 | 0.47 | [Formula]
Profit Factor         | 1.62 | 1.35 | 1.89 | [Formula]
Max DD %              | 12.6 | 10.2 | 15.8 | [Formula]
```

### Section 3: Permutation Test Chart (J2:J101)
Create 100 data points representing permutation distribution:
```
J2: Permutation Distribution
J3:J102: Random values between 0.4 and 0.6 (simulating p-value distribution)
```

Add **Bar Chart** → Place at A21

---

## Sheet 3: GOVERNANCE

### Section 1: Strategy Lifecycle (A3:E4)
```
Create 5 stage boxes:
A4: Idea    B4: Hypothesis    C4: Validation    D4: Paper    E4: Live

Current Status (A5): LIVE (green text)
```

### Section 2: Pre-Registered Criteria (A7:B12)
| Criterion | Value |
|-----------|-------|
| Min Expectancy (R) | 0.25 |
| Min Sample Size (trades) | 100 |
| Max Drawdown (R) | 15 |
| Min Profit Factor | 1.40 |
| Min PSR | 0.80 |

### Section 3: Decision Log (A14:D20)
```
Headers: Date | Decision | Signer | Rationale

Rows:
2026-04-22 | LIVE PROMOTION | R. Perekekeme | Validation passed; 450+ trades; Sharpe 1.45+
2026-04-15 | PAPER PROMOTION | Risk Committee | All criteria met; OOS expectancy confirmed
2026-03-20 | HYPOTHESIS APPROVED | Quant Team | Edge thesis validated on walk-forward
```

**Color Decision Column:**
- PROMOTION: Green text
- DEMOTION: Amber text
- RETIREMENT: Red text

### Section 4: Live Trade Tracker (A21:E30)
```
Headers: Date | Outcome | R Value | Cumulative R | Status

Track individual trades:
2026-05-18 | Win | +2.0 | 12.5 | ✓
2026-05-17 | Loss | -1.0 | 10.5 | ✗
2026-05-16 | Timeout | 0.0 | 11.5 | —
```

---

## Sheet 4: PORTFOLIO ALLOCATOR

### Section 1: Strategy Roster (A3:G8)
```
Headers: Strategy | Status | CAGR % | Sharpe | Max DD % | Weight % | Allocation $

Data:
ES 5m ORB | LIVE | 22.3 | 1.45 | 12.6 | 40% | $2,000,000
Order Block | PAPER | 18.5 | 1.12 | 15.2 | 30% | $1,500,000
Sector Momentum | HYPOTHESIS | 25.1 | 1.78 | 18.4 | 30% | $1,500,000
```

**Format:**
- Status column: Green for LIVE, Amber for PAPER, Gray for HYPOTHESIS
- Weight % as percentage format
- Allocation $ as currency

### Section 2: Correlation Matrix (A9:D12)
```
        | ES ORB | Order Block | Momentum
--------|--------|-------------|----------
ES ORB  | 1.00   | 0.45        | 0.12
Order Block | 0.45 | 1.00      | 0.28
Momentum | 0.12  | 0.28        | 1.00

Format:
- Values 0.5+ : Blue background (#4F8CFF)
- Diagonal: Gray background
- Center align all
```

### Section 3: Portfolio Summary (A15:B18)
```
Portfolio CAGR %           | 22.0%
Portfolio Sharpe           | 1.52
Portfolio Max DD %         | 14.2%
Diversification Ratio      | 1.18
```

**Format:** Bold, green text for values

### Charts to Add
1. **Pie Chart:** Allocation Weights (A3:B6) → Place at I9
2. **Scatter Chart:** Risk–Return Map (I15:K19) → Place at A21
   - X-axis: Risk (Max DD %)
   - Y-axis: Return (CAGR %)
   - Points: Each strategy + portfolio aggregate

---

## Shared Formatting Rules

### Color Scheme (Apply to All Sheets)
```
Dark Theme:
- Background: #0F1419 (dark navy)
- Panel: #161B22 (slightly lighter)
- Panel 2: #1C2230 (lighter still)
- Border: #2A3140
- Text: #E6EDF3 (light gray)
- Muted: #8B95A7 (muted gray)

Accent Colors:
- Accent: #4F8CFF (blue)
- Success: #26D07C (green)
- Danger: #EF4F56 (red)
- Warning: #F5B740 (amber)
- Info: #A37BF2 (purple)
```

### Text Styling
- **Headers:** Bold, 10-11px, muted color (#8B95A7)
- **Values:** 11-14px, light color (#E6EDF3)
- **Positive metrics:** Green (#26D07C), bold
- **Negative metrics:** Red (#EF4F56), bold

### Cell Borders
- All data cells: 1px solid #2A3140 (light border)
- Header rows: Bold text + background fill

---

## Data Import Instructions

### If Using Your Own Data

#### Trade Log Format (Create a new sheet called "TradeLog")
```
CSV Headers: Date, EntryPrice, ExitPrice, RiskAmount, RewardAmount, Outcome, RRatio

2026-05-18,100.50,102.50,100,150,Win,1.5
2026-05-17,99.25,98.25,50,50,Loss,1.0
2026-05-16,101.00,101.50,80,0,Timeout,0.0
```

Then use formulas to reference this data:
- `=COUNTIFS(TradeLog!$G:$G,"Win")` for win counts
- `=AVERAGEIF(TradeLog!$G:$G,"Win",TradeLog!$F:$F)` for avg winning RR

### Monte Carlo Simulation Data
For the Validation and Portfolio sheets' forecast charts, generate 1000 Monte Carlo paths:
```
Use Google Sheets add-on: "Simulation" or
Use formula: =NORMINV(RAND(), mean, std_dev) × sqrt(n_days)
```

---

## Advanced Features to Add

### Conditional Formatting
1. **Backtest Lab**: Color-code Win % green if >50%, red if <40%
2. **Governance**: Highlight trades below expected envelope in red
3. **Portfolio**: Highlight correlations >0.7 in red (high correlation warning)

### Data Validation (Dropdowns)
1. **Status column**: Restrict to [Idea, Hypothesis, Validation, Paper, Live, Watch, Retired]
2. **Outcome column**: Restrict to [Win, Loss, Timeout]
3. **Strategy selector**: List active strategies

### Pivot Tables
Create a **Pivot Table** sheet to analyze:
- Win rate by day-of-week
- Average expectancy by RR ratio
- Trade count by month

---

## Sharing & Collaboration

### Share Settings
1. Click **Share** → Set to **Editor** for team members
2. Turn on **Suggestion mode** for review workflows
3. Add comments on decision log entries for audit trail

### Real-Time Updates
- Use **IMPORTRANGE()** to link backtest data from another sheet
  ```
  =IMPORTRANGE("spreadsheet_url", "Backtest!A1:M50")
  ```

---

## Mobile View
- Pin the left 3 columns (Strategy/Status/Metrics) for mobile viewing
- Use **View** → **Freeze** → **1 column** to lock strategy names

---

## Need Help?

For dynamic calculations or complex charts, consider:
- **Google Sheets Add-ons**: Correlation Matrix, Data Fetcher, Charting extensions
- **Apps Script**: Automate daily trade uploads and metric recalculation
- **Google Forms**: Collect trade data directly into this sheet

---

**Last Updated:** May 18, 2026
**Version:** 1.0 (Quant-Level Professional Edition)
