# Suggestions for Homework:Application_Letter

1. Use `pathlib.Path` to handle paths instead of string concatenation.
2. Try to use vectorized `pandas` operations `apply`, but for I/O-intensive tasks like generating documents, processing row by row is reasonable.

# Suggestions for Homework: Big Data

1. Consider log-transforming skewed price/rent per-m2 for stabilization and easier coefficient interpretation.
2. Avoid in-place assignment on input dataframes; use df = df.copy() or df.loc[:, ...] before adding prediction columns.
