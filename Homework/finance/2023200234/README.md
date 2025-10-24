# Suggestions for Homework:Application_Letter

1. The code uses a Windows path: `output_main_dir = Path("C:/jupyter_code/homework/HW_School_Application")`. This will not work or may not be writable on Linux / cross-platform environments. It is recommended to use a relative path.

2. `DocxTemplate(template_path)` is created twice in the loop (it was already loaded once outside); this repeated loading is unnecessary. It is recommended to load the template once externally, then create fresh instances.

3. Add necessary comments to improve code readability.

# Suggestions for Homework: Big Data

Your assignment is well-structured, with clear data processing, modeling, and result comparison. The feature engineering and model interpretation are thoughtful. Remember to handle outliers before modeling;