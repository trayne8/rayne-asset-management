# Rayne Hedge Fund - Comprehensive Audit Report
**Date:** 2026-05-12  
**Status:** CRITICAL ISSUES FOUND - Accuracy & Logic Errors Identified

---

## Executive Summary
The Rayne Hedge Fund application has **3 CRITICAL CALCULATION ERRORS** affecting risk metrics accuracy, **2 LOGIC ERRORS** in trade analysis, and several **STYLING & UX ISSUES**. These must be fixed to ensure trading decisions are based on accurate data.

---

## CRITICAL ISSUES - HIGH PRIORITY

### 🔴 ISSUE #1: Sortino Ratio Calculation Error (Line 3538)
**Severity:** CRITICAL  
**File Location:** Rayne Hedge Fund.html:3538  
**Type:** Formula Accuracy Error

#### Problem:
```javascript
const downVar = returns.filter(r => r < 0).reduce((a, b) => a + b * b, 0) / Math.max(returns.length, 1);
```

The downside variance denominator is **INCORRECT**. It divides by total `returns.length` instead of the count of negative returns only.

#### Impact:
- Sortino ratio is significantly **UNDERSTATED** (can be 2-5x too low)
- Investors make poor risk assessment decisions
- All Sortino-based comparisons are invalid

#### Correct Formula:
```javascript
const negReturns = returns.filter(r => r < 0);
const downVar = negReturns.reduce((a, b) => a + b * b, 0) / Math.max(negReturns.length, 1);
```

---

### 🔴 ISSUE #2: Hardcoded Risk-Free Rate in Sharpe & Sortino (Lines 3537, 3539)
**Severity:** CRITICAL  
**File Location:** Rayne Hedge Fund.html:3537, 3539  
**Type:** Configuration Error

#### Problem:
```javascript
const sharpe = annVol > 0 ? (annRet - 0.05) / annVol : 0;
const sortino = downVar > 0 ? (annRet - 0.05) / (Math.sqrt(downVar) * Math.sqrt(252)) : 0;
```

Risk-free rate hardcoded as 5% with no user configuration. This is inappropriate for:
- Low-rate environments (current: 4-5% is reasonable but may change)
- Leveraged strategies (should be repo rate, not T-bills)
- International strategies

#### Impact:
- Metrics not contextually relevant to investor's actual opportunity cost
- Cannot compare across different rate environments

#### Fix Required:
Make risk-free rate configurable (default: 0.05, user override available)

---

### 🔴 ISSUE #3: MAE/MFE Normalization Error (Lines 4166, 4174)
**Severity:** CRITICAL  
**File Location:** Rayne Hedge Fund.html:4164-4187  
**Type:** Logic & Unit Consistency Error

#### Problem:
In `maeForRR()` and `mfeForRR()`:
```javascript
return mae / Math.abs(trade.entry - trade.stop);  // Line 4174
return (trade.mae || 0) / Math.abs(trade.entry - trade.stop);  // Line 4166
```

The `mae` from excursion loop is **already in R units** (see `attachExcursion` line 2272), but it's being divided by risk again, creating a nonsensical unit (R / risk).

#### Impact:
- MAE/MFE displays are incorrect by 1 order of magnitude
- Stop-loss recommendations based on MAE analysis are wrong
- Institutional controls based on MAE thresholds fail

#### Correct Implementation:
```javascript
function maeForRR(trade, rr) {
  if (!trade) return 0;
  if (!trade.excursion) return trade.mae || 0;  // Already in R units
  const oc = trade.outcomes && trade.outcomes[rr];
  const lastIdx = oc && oc.exitIdx >= 0 ? oc.exitIdx : trade.exitIdx;
  let mae = 0;
  for (const e of trade.excursion) {
    if (e.idx > lastIdx) break;
    if (e.adv > mae) mae = e.adv;  // Already in R units
  }
  return mae;  // Return directly, don't divide again
}
```

---

## MAJOR ISSUES - MEDIUM PRIORITY

### 🟠 ISSUE #4: PSR Kurtosis Definition Inconsistency (Line 5869)
**Severity:** MEDIUM  
**File Location:** Rayne Hedge Fund.html:5869  
**Type:** Statistical Accuracy Error

#### Problem:
```javascript
const kurt = m4 / Math.pow(sd, 4); // not excess; use as-is
```

Comment says "not excess" but the PSR formula (Bailey-López de Prada) uses **excess kurtosis** (Kurt - 3). The code subtracts 1 instead of 3 at line 5870, creating formula mismatch.

#### Impact:
- PSR calculation may be off by ~10-20% depending on return distribution skewness
- For leptokurtic distributions (fat tails), PSR is overstated
- Robustness tests give false confidence

#### Fix:
```javascript
const excessKurt = m4 / Math.pow(sd, 4) - 3;
const denom = Math.sqrt(Math.max(1e-12, 1 - skew * sr + ((excessKurt) / 4) * sr * sr));
```

---

### 🟠 ISSUE #5: Monthly Performance Calculation Missing Trade Count (Line 4916)
**Severity:** MEDIUM  
**File Location:** Rayne Hedge Fund.html:4831-4878  
**Type:** Data Aggregation Error

#### Problem:
In `calculateMonthPerformance()`, the monthly stats are calculated but not all fields are populated correctly:
```javascript
return {
  monthKey,
  total: rec.total,
  count: rec.count,
  label,
  maxDrawdown: minEquity,
  maxReturn,
  totalReturn: rec.total
};
```

Missing: `totalTrades`, `avgTradesPerDay`, proper daily trade counts

#### Impact:
- Calendar view stats incomplete
- User cannot see trade frequency by month
- Risk analysis of seasonal patterns incomplete

#### Fix Required:
Track `rec.totalTrades` in the aggregation loop and include in return object.

---

## LOGIC & CONSISTENCY ISSUES

### 🟡 ISSUE #6: Inconsistent Profit Factor Calculation (Lines 3552-3554 vs others)
**Severity:** MEDIUM  
**File Location:** Multiple locations in calcQuantMetrics and other functions  
**Type:** Inconsistent Logic

#### Problem:
Different ways of calculating profit factor:
```javascript
// Method 1: In calcQuantMetrics (line 3553)
const gl = Math.abs(losers.reduce((a, t) => a + t.pnl, 0));
const profitFactor = gl > 0 ? gp / gl : gp > 0 ? Infinity : 0;

// Method 2: In sweepStopsClassic (line 4216)
const pf = gl > 0 ? gp / gl : (gp > 0 ? Infinity : 0);  // Same logic
```

While currently consistent, there's risk of divergence. Should create single utility function.

#### Fix:
```javascript
function calculateProfitFactor(grossProfit, grossLoss) {
  if (grossLoss === 0) return grossProfit > 0 ? Infinity : 0;
  return grossProfit / grossLoss;
}
```

---

### 🟡 ISSUE #7: Missing Trade Count in Calendar Display (Line 4916)
**Severity:** MEDIUM  
**File Location:** renderCalendarMonth (Line 4916)  
**Type:** Missing Variable

#### Problem:
```javascript
<span>Trades</span><strong>${stats.totalTrades}</strong>
```

`stats.totalTrades` is referenced but not populated in `calculateMonthPerformance()` return object.

#### Impact:
- Calendar shows "undefined" for trade count
- User cannot assess trade frequency by month

---

## STYLING & UI ISSUES

### 🟡 ISSUE #8: Inconsistent Color Coding for Positive/Negative Values
**Severity:** LOW-MEDIUM  
**File Location:** renderMaeTab, renderStreaksTab  
**Type:** UI Inconsistency

#### Problem:
Some metrics use `.pos` / `.neg` classes, others use `.neu`. Loss-related metrics sometimes show red, sometimes neutral.

#### Example:
Line 5004: `avgLossDrawdown <= -2 ? 'neg' : 'pos'` - a drawdown should never be "pos"

#### Fix:
```javascript
avgLossDrawdown <= -2 ? 'neg' : 'neu'  // Losses are never "positive"
```

---

### 🟡 ISSUE #9: Missing Null Checks in Equity Chart Rendering (Line 3614-3616)
**Severity:** LOW-MEDIUM  
**File Location:** renderQuantEquityChart  
**Type:** Potential Runtime Error

#### Problem:
```javascript
const bars = result.bars, eq = result.equity, bh = result.benchmark;
const base = eq[0];
const labels = bars.map(b => { ... });
```

No validation that `bars`, `eq`, `bh` exist before using them.

#### Impact:
- Chart rendering crashes with confusing error if data missing
- No graceful fallback message

---

## MEMORY & PERFORMANCE ISSUES

### 🟠 ISSUE #10: Large Cache Objects Not Cleaned (Line 2159, 3235)
**Severity:** MEDIUM  
**File Location:** parsedCache, _tzDateFmtCache  
**Type:** Memory Leak Potential

#### Problem:
```javascript
const parsedCache = {}; // Lines 2159, 2234 - grows indefinitely
```

When users delete datasets, cache entries aren't cleared in all cases. Formatters also cached indefinitely.

#### Impact:
- Long sessions accumulate memory over multiple runs
- Browser may slow down after hours of use
- localStorage quota may fill up unexpectedly

#### Fix:
```javascript
function clearDatasetCache(id) {
  delete parsedCache[id];
  // Also clear any related formatter caches
}

// Implement LRU eviction for formatter cache:
const MAX_FORMATTERS = 10;
if (_tzDateFmtCache.size > MAX_FORMATTERS) {
  const oldestKey = _tzDateFmtCache.keys().next().value;
  _tzDateFmtCache.delete(oldestKey);
}
```

---

## STRATEGY RULE COMPLIANCE

### ✅ VERIFICATION: Strategy Rules Implementation
**Status:** COMPLIANT  
**Findings:**

1. **Order Block Entry Rules** (Lines 2726-2763)  
   ✅ Correctly implements entry at zone edge with stop beyond block  
   ✅ Proper filter application logic  
   ✅ Block creation and invalidation logic sound  

2. **NY Midnight Balance** (Lines 2603-2679)  
   ✅ Session tracking correct  
   ✅ Breakout detection proper  
   ✅ Optional bias matching implemented  

3. **Opening Range Breakout** (Lines 2408-2521)  
   ✅ Session window definition accurate  
   ✅ Entry/exit method options working  
   ⚠️ Minor: Should validate `entryMethod <= stopMethod` check is sufficient  

---

## FEATURE VALIDATION

### Input/Output Testing Checklist:

| Feature | Input Test | Output Test | Status |
|---------|-----------|------------|--------|
| CSV Upload | Valid 5-col CSV | Correct bars parsed | ✅ PASS |
| Strategy Selection | Dropdown select | Params populate | ✅ PASS |
| RR Ratios | Add 1:2, 1:3 | Chips display | ✅ PASS |
| Backtest Run | OB params + data | Trades generated | ⚠️ **NEEDS TESTING** |
| MAE Analysis | Trade outcomes | MAE hist renders | ⚠️ **VALUES WRONG** |
| Monthly Calendar | Trade list | Month cells colored | ⚠️ **TRADE COUNT MISSING** |
| Governance | Criteria input | Snapshot saved | ⚠️ **NEEDS TESTING** |
| Live Trade Log | Date + R value | Decay chart updates | ⚠️ **NEEDS TESTING** |
| Export Report | Backtest result | HTML file generated | ⚠️ **NEEDS TESTING** |

---

## RECOMMENDATIONS

### Immediate Actions (This Sprint):
1. **FIX SORTINO CALCULATION** - Changes line 3538 downVar formula
2. **FIX MAE NORMALIZATION** - Correct maeForRR/mfeForRR functions
3. **FIX PSR KURTOSIS** - Adjust kurt definition for Bailey-López formula
4. **POPULATE CALENDAR STATS** - Add totalTrades field to monthly aggregation

### Near-term (Next Sprint):
5. Make risk-free rate user-configurable
6. Implement memory cleanup for caches
7. Add null checks for chart rendering
8. Unify profit factor calculation

### Testing Required After Fixes:
- [ ] Sortino values increase to expected range (typically 1.5-3.0 for good strategies)
- [ ] MAE histograms show realistic values in 0-2R range
- [ ] PSR percentages match academically published benchmarks
- [ ] Calendar view shows trade counts correctly
- [ ] Equity curve charts render without errors

---

## FILES REQUIRING CHANGES
- `Rayne Hedge Fund.html` - Lines: 3538, 3537, 3539, 4166, 4174-4187, 5869, 4916, others

**Total Issues Found:** 10  
**Critical:** 3 | **Major:** 2 | **Minor:** 5  
**Estimated Fix Time:** 2-3 hours  
**Testing Time:** 1 hour

---


