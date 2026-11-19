# Hester unseen evaluation

Fee: 5 bps per side. Initial capital: $100,000.00.

```text
                                         gross              net
start                               2023-10-09       2023-10-09
end                                 2026-10-06       2026-10-06
sessions                                   751              751
initial_equity                          100000           100000
final_equity                     175372.787944    158587.697387
pnl                               75372.787944     58587.697387
total_return_pct                     75.372788        58.587697
cagr_pct                             20.743053        16.734963
annualized_volatility_pct            23.764645        23.757323
sharpe                                0.911895         0.769924
max_drawdown_pct                    -21.241257       -22.315281
best_day_pct                         10.595285        10.578525
worst_day_pct                        -7.978421        -7.980406
closed_trades                              203              203
win_rate_pct                           40.8867        38.916256
profit_factor                         1.298961         1.236767
average_trade_return_pct              0.676775         0.576148
average_holding_calendar_days         7.921182         7.921182
average_exposure_pct                 73.914218        73.925593
fees_paid                                  0.0     14476.866426
traded_notional                30573246.104298  28953732.852702
```

## Accounting assumptions

- fee_bps_per_side: 5
- initial_capital: 100000
- annual_risk_free_rate: 0
- annualization_sessions: 252
- execution: Prior close signal; next session open fills; final close liquidation
- warmup: Last 21 pre-holdout closes; start flat; no warm-up P&L
- sizing: Preserve surviving shares; scale new buys pro rata to available cash including fees
- comparison: Independent gross and net runs of unchanged TrendStrategy
- exclusions: No slippage, spread, market impact, cash interest, dividends or explicit corporate action processing; prices used as supplied

CAGR and volatility use 252 sessions/year. Sharpe uses sample daily standard deviation and the configured risk-free rate. Drawdown includes initial capital. Trade returns include both entry and exit fees. Final liquidation trades count in all statistics. Exposure is measured at the close before final liquidation. A null profit factor means no losing trades.

The separate runs can differ in sizing because fees reduce available cash. Gross-minus-net terminal wealth includes both paid fees and their subsequent compounding effect.

The CSV price adjustment status is unverified. Results are a price-only simulation under these assumptions, not a reproduction of the writeup's backtest.