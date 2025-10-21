# Suggestions for Homework:Application_Letter

1. The `template` needs to be reloaded in each iteration.
2. Split the function into multiple smaller functions with specific responsibilities.

# Suggestions for Homework: Big Data

1. Refrain from using Windows-style absolute paths (e.g., `D:/...`) in the Notebook. It is recommended to adopt relative paths (e.g., `./data/...`) or utilize `pathlib.Path` with project root configuration (e.g., `Path(project_root) / 'data' / '...'`) for better portability and maintainability.
2. When applying `C(community_name)`, document the sample size for each category. Consider consolidating low-frequency categories into an "Other" group to reduce parameter dimensionality and enhance model stability.