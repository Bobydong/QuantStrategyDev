# The dataset is 10 years, split 70/30

10 years of daily ticker data for 6 stocks split into:

7 years of training data used for backtesting and preliminary evaluation. 

3 years of unseen data to do final "forward-looking" evaluation. 

## Asset-to-Stock Mapping Reference

Reference table to map the anonymized asset identifiers to their original stock datasets:

| Asset ID | Original Filename | Underlying Stock / Asset |
|---|---|---|
| **Asset_A** | `HistoricalData_appl.csv` | Apple Inc. (AAPL) |
| **Asset_B** | `HistoricalData_Boe.csv` | Boeing Co. (BA) |
| **Asset_C** | `HistoricalData_meta.csv` | Meta Platforms, Inc. (META) |
| **Asset_D** | `HistoricalData_tsla.csv` | Tesla, Inc. (TSLA) |
| **Asset_E** | `HistoricalData_sbux.csv` | Starbucks Corporation (SBUX) |
| **Asset_F** | `HistoricalData_Ford.csv` | Ford Motor Company (F) |
