### HW1&2 (University Applications Letters Generator) Score: 




| Student ID | Name   | number | group | HW1  | HW2: Score |
| ---------- | ------ | ------ | ----- | ---- | ---------- |
| 2023200593 | 赵蔚   | 0      | 1     | √    | 8.5        |
| 2023201778 | 顾梓民 | 1      | 1     | √    | 8.5        |
| 2023200604 | 路畅宇 | 2      | 1     | √    | 8.5        |
| 2023201777 | 许家淼 | 3      | 1     | √    | 8.5        |
| 2023200740 | 陈君昊 | 4      | 2     | √    | 8.5        |
| 2023200753 | 白瑞睿 | 5      | 2     | √    | 8.5        |
| 2023200769 | 郑瑜   | 6      | 2     | √    | 8.5        |
| 2023201779 | 孙一丹 | 7      | /     | /    | /          |
| 2023200778 | 贺佳乐 | 8      | 3     | √    | 9          |
| 2023201782 | 柏欣妍 | 9      | 3     | √    | 8.5        |
| 2023200609 | 王一舟 | 10     | 3     | √    | 9          |
| 2023201781 | 王子涵 | 11     | 3     | √    | 9          |
| 2023200697 | 陶绪志 | 12     | 4     | √    | 9          |
| 2023200727 | 吴宇茜 | 13     | 4     | √    | 8.5        |
| 2023200725 | 潘晓语 | 14     | 4     | √    | 8.5        |
| 2023201780 | 袁博辰 | 15     | 4     | √    | 9          |
| 2023200595 | 高福玉 | 16     | 5     | √    | 8.5        |
| 2023200761 | 黄皆瑞 | 17     | 5     | √    | 8.5        |
| 2023200721 | 李昕芮 | 18     | 5     | √    | 8.5        |



- **Key Points for Score**

  - **Complete the base task:** Ensure your code can generate application letters for 30 universities * 3 majors * journals * skills.
  - **Follow the workflow:** We expect you to follow the workflow strictly.
  - **Original work:** *DO NOT* copy any code from your classmates.

- **Code Guide:** Refer to the Google Python Style Guide for elegant code writing

  - Chinese version: https://zh-google-styleguide.readthedocs.io/en/latest/google-python-styleguide/python_language_rules.html
  - English version: https://github.com/google/styleguide
  - Sargent Code: https://github.com/QuantEcon/lecture-python-programming.notebooks/blob/main/writing_good_code.ipynb

- **Tips for HW2**

  - **Use relative paths:** Instead of absolute paths, use <u>relative paths</u> to make your code more flexible and easier to maintain.

  - **Meaningful variable names:** Use proper and descriptive variable names that convey their purpose, which will definitely make it easier for team collaboration and others to understand your code. Try your best to avoid using generic names like `xxx1`, `xxx2`, etc.

  - **Writing comments:** Add comments to your code to make it more readable and understandable. Be careful that we always leave a space after the symbol `#` for a full line of comments. And Symbol `#` often need to be four spaces away from the code, for comments after the current line of code. Here is an example.

    - ```python
      # 这是一整行的注释
      print("HELLO WORLD!")
      
      print("DAY DAY UP!")    # 这是行内注释
      
      def calculate_add(x, y):
      """对两个数进行相加
      
      Args:
      	x (int): 第一个加数
      	y (int): 第二个加数
      
      Returns:
      	int: 两个数的和
      """
      	return a + b
      ```

  - **File process:** Use `os` to do file or path work. To get the complete path, we tend to connect via `os` to automatically match the differences in paths between systems, such as `Windows`, `Linux`, `Mac`. Before reading or writing a file or path, you can use `os.path.exists(path)` or `os.path.isfile(path)` to ensure it exists.

  - **Excel list: **We anticipate generating a single `Excel list` for your generator's loop; a sample `pandas Dataframe` structure is provided below.

    >| **Universities**           | **Areas**  | **Journals**       | **Skills**         |
    >| -------------------------- | ---------- | ------------------ | ------------------ |
    >| ***<u>Examples</u>*:**     |            | depends on `Areas` | depends on `Areas` |
    >| Harvard University         | Economics  | AER                | Econometrics       |
    >| Harvard University         | Economics  | JPE                | Econometrics       |
    >| Harvard University         | Finance    | JF                 | Computer Skills    |
    >| Harvard University         | Management | MS                 | Data Analysis      |
    >| University of Pennsylvania | Economics  | AER                | Econometrics       |
    >| ......                     | ......     | ......             | ......             |
  
  - **Provide your output feedback:** Use `print` statements or `tqdm` to provide feedback on the progress of your loops, making it easier to understand how your code is executing. You can easily identify endless loops.
  
  - **Separate commands and code:** In `.ipynb` files, keep commands (e.g., `!pip install xxx` or `%pip install xxx`) and Python code in separate cells to maintain organization and clarity. You could also make `markdown` cells to make your code structure clearer and more readable.
  
  - **Random algorithm:** We expect you to use Python `random` to draw 30 universities from a list, in which process you can use `random.Random(seed)` to ensure replication.
