# 🚀 QUICK START GUIDE
## Rayne Hedge Fund Quant Dashboard (Excel + Google Sheets)

---

## ⚡ 5-Minute Setup

### Option 1: Excel (Fastest)
```
1. Open: Rayne_Hedge_Fund_Quant_Dashboard.xlsx
2. Review the 4 sheets at bottom
3. Done! Sample data pre-filled
```

### Option 2: Google Sheets (Best for Collaboration)
```
1. Go to Google Drive
2. Right-click → Upload → Rayne_Hedge_Fund_Quant_Dashboard.xlsx
3. Open file
4. Google auto-converts all formulas
5. Share link with team
```

### Option 3: Manual Setup (Most Control)
```
1. Follow: GOOGLE_SHEETS_SETUP_GUIDE.md
2. Takes ~30 minutes
3. Get exactly what you want
```

---

## 📊 What's Inside

### 4 Professional Sheets

| Sheet | Purpose | Key Metrics |
|-------|---------|-------------|
| **Backtest Lab** | Test strategies across RR ratios | Win %, Profit Factor, Expectancy, Sharpe |
| **Validation Suite** | Institutional stat validation | Permutation p-value, PSR, Bootstrap CIs |
| **Governance** | Lifecycle + decision audit trail | Status, Pre-reg criteria, Live trades |
| **Portfolio Allocator** | Multi-strategy optimization | Correlation matrix, allocation weights, efficient frontier |

**All data is color-coded for quick insight:**
- 🟢 Green = Success/Wins/PASS
- 🔴 Red = Losses/FAIL
- 🟡 Amber = Caution/Pending
- 🔵 Blue = Information/Accent

---

## 🔧 Import Your Data (2 Steps)

### Step 1: Create Trade Log
```
1. New sheet → Name it "TradeLog"
2. Paste columns: Date, Entry, Exit, Risk, Reward, Outcome, RR, Strategy
3. Add your trades (sample: SAMPLE_TRADE_LOG.csv)
```

### Step 2: Update Formulas
In **Backtest Lab**, row 7+:
```
Before: =COUNTIFS(TradeLog!$C:$C,"Win")
After:  =COUNTIFS(TradeLog!$G:$G,"Win")
```

**Charts update automatically** ✓

---

## 📈 Key Features by Sheet

### BACKTEST LAB
- RR Summary (1.0 to 4.0 ratios)
- Equity curve chart
- Win/Loss pie chart
- Key metrics panel

**What to do:** Upload trade log → all metrics calculate automatically

---

### VALIDATION SUITE
- 4-point validation checklist (PASS/WARNING/FAIL)
- Bootstrap confidence intervals
- Permutation test results
- Robustness to slippage analysis

**What to do:** Input your permutation test results from Python → get institutional-grade p-values

---

### GOVERNANCE
- Strategy lifecycle stages (Idea → Live)
- Pre-registered acceptance criteria
- Decision log (permanent audit trail)
- Live trade tracker with decay monitoring

**What to do:** 
1. Record promotions/demotions with rationale
2. Add live trades daily
3. Monitor if performance stays in envelope

---

### PORTFOLIO ALLOCATOR
- Strategy roster (all live/paper strategies)
- Correlation matrix (click to edit)
- Risk–Return scatter chart
- Allocation pie chart
- Portfolio metrics

**What to do:**
1. Add your strategies to roster
2. Review/update correlations
3. Run "Build Portfolio" → get allocation weights

---

## 💡 Common Workflows

### Workflow 1: Test a New Strategy
```
1. Go to Backtest Lab sheet
2. Change strategy dropdown
3. Upload trade log
4. Formulas auto-calculate
5. Review metrics vs thresholds
```

### Workflow 2: Validate Edge (Research)
```
1. Run 200+ permutation tests (Python)
2. Go to Validation Suite
3. Input: p-value, PSR, CI bounds
4. Check: All green? Ready for promotion
```

### Workflow 3: Promote Strategy to Live
```
1. Go to Governance sheet
2. Fill in "Pre-reg Criteria" section
3. Fill in "Decision Log" with rationale + signer
4. Move strategy to "Live" column
5. Audit trail saved forever
```

### Workflow 4: Build Multi-Strategy Portfolio
```
1. Go to Portfolio Allocator
2. Add 3-5 strategies to roster
3. Adjust correlation matrix
4. Click chart → see efficient frontier
5. Final weights show allocation $
```

### Workflow 5: Monitor Live Performance
```
1. Daily: Add live trades to Governance sheet
2. Watch cumulative R chart vs backtest envelope
3. If below lower band 30+ trades → review or retire
4. Every week: Update decision log
```

---

## 🎯 Sample Metrics (Already Pre-Filled)

**Backtest Lab:** ES 5m ORB strategy
- Total Return: 47.2%
- CAGR: 22.3%
- Win Rate: 41%
- Sharpe: 1.45
- Max DD: 12.6%

**Validation:** Gold-standard tests
- Permutation p-value: 0.032 ✓ (edge real)
- PSR: 0.87 ✓ (likely positive Sharpe)
- Robustness at 2-tick slippage: 0.94x ⚠ (slight degradation)

**Portfolio:** 3-strategy blend
- CAGR: 22.0% (vs individual 22.3%, slight drag from correlation)
- Sharpe: 1.52 (improved via diversification)
- Allocation: 40% ORB / 30% Order Block / 30% Momentum

---

## 📁 Files Included

```
📦 Rayne Asset Management/
├── Rayne_Hedge_Fund_Quant_Dashboard.xlsx    ← Main workbook
├── SAMPLE_TRADE_LOG.csv                     ← Example trade data
├── README_QUANT_DASHBOARD.md                ← Full documentation
├── GOOGLE_SHEETS_SETUP_GUIDE.md             ← Sheet-by-sheet guide
└── QUICK_START_GUIDE.md                     ← This file
```

---

## ❓ FAQ

**Q: Can I use this without my own data?**  
A: Yes! Sample data pre-filled so you can see how it works immediately.

**Q: Does Google Sheets work as well as Excel?**  
A: Yes! Google auto-converts all formulas. Collaboration is easier in Sheets.

**Q: Can I add more strategies?**  
A: Absolutely! Duplicate rows in Governance → roster auto-pulls to Portfolio.

**Q: How do I handle multiple RR ratios?**  
A: Backtest Lab has 5 pre-built RR levels (1, 1.5, 2, 3, 4). Duplicate rows as needed.

**Q: What if my trade log format is different?**  
A: Update the column references in formulas (e.g., `TradeLog!$G:$G` = your "Outcome" column).

**Q: Can I export charts as images for reports?**  
A: Yes! Right-click chart → "Download as image" → PNG/PDF

**Q: Is this suitable for institutional use?**  
A: Yes! Governance sheet has audit trail and pre-registration for compliance.

---

## 🎨 Customize the Look

### Change colors in Google Sheets:
1. Select cell/range
2. Format → Fill color → Pick color
3. Our theme: Dark navy background (#0F1419)

### Add your logo:
1. Insert → Image → Upload logo
2. Position at top-left of Backtest Lab

### Change metrics shown:
1. Delete unwanted rows in key metrics panels
2. Add your own metrics (just duplicate row + change formula)

---

## 📞 Next Steps

### Immediate (Today)
- [ ] Open Excel or Google Sheets version
- [ ] Review the 4 sheets
- [ ] Understand sample data flow

### Short-term (This Week)
- [ ] Prepare your trade data (CSV format)
- [ ] Create TradeLog sheet
- [ ] Plug in actual trades
- [ ] Verify charts update

### Medium-term (This Month)
- [ ] Add validation test results
- [ ] Set pre-registered criteria
- [ ] Promote strategies through lifecycle
- [ ] Build portfolio allocation

### Long-term (Ongoing)
- [ ] Add live trades daily
- [ ] Review decision log weekly
- [ ] Monitor decay vs backtest envelope
- [ ] Share with team (Google Sheets)

---

## 💼 For Your Team

### Share with Stakeholders
```
1. Google Sheets version (easier for viewers)
2. Share → Set permissions → View only
3. Send link to portfolio manager + risk committee
```

### Setup Automated Updates
```
1. Google Forms → collects trade entries
2. Form auto-populates TradeLog sheet
3. All metrics update in real-time
4. Notification email daily
```

### Create Reports
```
1. Google Sheets → File → Download as PDF
2. Charts/tables stay formatted
3. Perfect for investor reports or Monday reviews
```

---

## ⚙️ Pro Tips

### Tip 1: Use Conditional Formatting
- Highlight Win % green if >50%, red if <40%
- Alerts when correlations >0.7

### Tip 2: Freeze Header Rows
- View → Freeze → Top 2 rows
- Headers stay visible when scrolling

### Tip 3: Create Pivot Tables
- Right-click any data table
- "Pivot table" → Analyze by day-of-week, month, etc.

### Tip 4: Daily Trade Entry via Google Form
- Form → Auto-populates TradeLog
- Dashboard updates instantly
- No manual copy/paste

### Tip 5: Version Control
- Right-click file (Google Sheets) → "Version history"
- Snapshots of sheet before each change
- Roll back if needed

---

## 📚 Learn More

**For detailed setup:** See `GOOGLE_SHEETS_SETUP_GUIDE.md`

**For full documentation:** See `README_QUANT_DASHBOARD.md`

**For sample data format:** See `SAMPLE_TRADE_LOG.csv`

---

## ✅ Success Checklist

- [ ] Dashboard opened
- [ ] All 4 sheets reviewed
- [ ] Charts rendering correctly
- [ ] Trade log data uploaded
- [ ] Formulas updated
- [ ] Metrics displaying correctly
- [ ] Colors making sense
- [ ] Ready to add live trades
- [ ] Shared with team (if applicable)
- [ ] Bookmarked for daily use

---

**You're ready to go! Start with the Backtest Lab sheet and work through the workflow above.**

*Questions? Check README_QUANT_DASHBOARD.md for detailed explanations.*

---

**Version:** 1.0 Professional Edition  
**Created:** May 18, 2026  
**For:** Senior Quantitative Analyst  
**Quality:** Production-ready
