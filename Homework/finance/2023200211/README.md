# Suggestions for Homework:Application_Letter

1. Use pathlib.Path to handle paths

2. Reduce traces of AI-generated code

3. Avoid wrapping import statements in try/except blocks, and refrain from repeatedly `using subprocess.run([python -m pip install ...])` in notebooks.

# Suggestions for Homework: Big Data

1. Refrain from redefining functions or variables with the same name multiple times within the Notebook, as this increases reading and debugging complexity.
2. When performing sampling or using algorithms with inherent randomness (e.g., machine learning models), maintain a fixed random_state and document it at key steps to ensure reproducible results.
3. For data preprocessing functions, always operate on a copy of the DataFrame (e.g., df = df.copy()) to avoid unintended modifications to the original dataset.
