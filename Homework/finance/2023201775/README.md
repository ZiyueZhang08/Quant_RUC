# Suggestions for Homework:Application_Letter

1. Use `pathlib.Path` to handle paths

2. Try to use vectorized `pandas` operations `apply`, but for I/O-intensive tasks like generating documents, processing row by row is reasonable.

3. Load the template out of the loop to improve efficiency (loaded once and used repeatedly).

# Suggestions for Homework: Big Data

1. Please use English filenames and reorganize your homework submissions into separate folders for each assignment to maintain a clear project structure.
2. Function/variable alignment issue: The `detect_outliers_iqr` function is designed to accept a `Series` but contains hardcoded references to `df_house/df_rent`, which may cause confusion or errors. Consider refactoring it to work consistently with the input parameter.
3. Regression modeling refinement: For better clarity in your model formula, explicitly mark categorical variables using the appropriate notation (e.g., `C(location)`). This ensures proper interpretation and treatment of categorical predictors in statistical models.
