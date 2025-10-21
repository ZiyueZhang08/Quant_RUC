# Suggestions for Homework: Big Data

1. Extract Common Utilities into a Shared Module
Consolidate frequently used functions (e.g., data parsing, unit conversion, logging, and plotting) into a shared utility module. This reduces code duplication across notebooks, enhances maintainability, and streamlines development.
2. Optimize DataFrame Iteration for Large Datasets
Avoid using iterrows for large DataFrames due to its poor performance. Instead:
- Prefer vectorized operations or `Series.apply` with lightweight, deterministic parsing functions.
- Perform column-wise preprocessing (e.g., using `str.contains` or `str.extract`) to minimize Python-level loops and improve efficiency.
