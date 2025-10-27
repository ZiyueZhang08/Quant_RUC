> [!IMPORTANT]
>
> ### **This document contains your homework ratings and all associated comments.**



#### HW1: sololearn certificates

- Done


#### HW2: University Applications Letters Generator

- Score: 8.5
- Comments:
    - It is better to place `random.seed` inside `main`:
      ```
      if __name__ == "__main__":
          random.seed(42)  # 仅在直接运行时生效
          main()
      ```
    - It's better to have document template in .docx rather than putting it directly in the code.


#### HW3: My_Data_My_Model

- Score: 8.5
- Comments:
    - In `.ipynb` files, keep commands (e.g., `!pip install xxx` or `%pip install xxx`) and Python code in separate cells to maintain organization and clarity.
    - In this homework we prefer to identify `next page` button rather than revise the parameter in you `url` path.
    - You are expected to use `statsmodels` library for your linear regression model for data statistics (ordinary least squares, t-test, P-value etc.), while `sklearn` focus on machine learning algorithms and predictions. (Recommend)
    - Great job in data visualization, but in the figure `Figure A, Figure B, Figure C, Figure D` the axhline is not relative. (BE AWARE)
    - Your comments on how to select the models?
