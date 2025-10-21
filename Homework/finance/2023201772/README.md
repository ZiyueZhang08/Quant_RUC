# Suggestions for Homework: Big Data

1. Clarify Out-of-Distribution (OOD) Data Handling Strategy

Currently, OOD instances are only flagged without specifying subsequent processing methods (e.g., removal or truncation). A clear handling strategy should be established to ensure consistency during model training.

2. Address Categorical Treatment of Location Variable

Treating location as continuous numerical values (e.g., directly using 1, 2, 3) implicitly introduces ordinal and distance assumptions, which may distort regional effect estimates. This is particularly problematic when incorporating polynomial or interaction terms, as it can lead to misleading interpretations.

3. Revise Feature Engineering Sequence for Polynomial Features
In nonlinear_regression, applying `PolynomialFeatures` directly to `[space, location]` generates problematic terms like `location²` and `space × location`. For proper categorical handling:
   - First convert location to one-hot encoded features
   - Then use dedicated interaction generators or explicitly construct meaningful cross terms
   - This prevents mathematically invalid location quadratic terms while maintaining interpretable feature interactions
