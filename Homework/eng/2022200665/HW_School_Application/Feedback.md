# Homework Feedback
The overall score of your work is 8/10.

## Advice
1. The DocxTemplate is loaded outside the loop, which causes all documents after the first one to be based on the previously rendered document rather than the original template. This will result in incorrect or duplicated content.
2. Please submit your work as a Jupyter Notebook (.ipynb) instead of a Python script (.py). This allows us to see the execution results and outputs of each code cell, which is important for grading.
3. Add try-except around the file generation loop to catch and report individual failures without stopping the entire batch.

TA: Xue Jiayi
