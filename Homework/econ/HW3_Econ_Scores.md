## HW3: Selenium&DataAnalysis Score Report


| Student ID   | Name   | Number | Group | HW3  |
|--------------|--------|--------|-------|------|
| 2023200593   | 赵蔚   | 0      | 1     | 9    |
| 2023200595   | 高福玉 | 16     | 5     | 8.5  |
| 2023200604   | 路畅宇 | 2      | 1     | 8    |
| 2023200609   | 王一舟 | 10     | 3     | 8    |
| 2023200697   | 陶绪志 | 12     | 4     | 8.5  |
| 2023200721   | 李昕芮 | 18     | 5     | 9    |
| 2023200725   | 潘晓语 | 14     | 4     | 8.5  |
| 2023200727   | 吴宇茜 | 13     | 4     | 8.5  |
| 2023200740   | 陈君昊 | 4      | 2     | 9.5  |
| 2023200753   | 白瑞睿 | 5      | 2     | 8.5  |
| 2023200761   | 黄皆瑞 | 17     | 5     | 9    |
| 2023200769   | 郑瑜   | 6      | 2     | 9    |
| 2023200778   | 贺佳乐 | 8      | 3     | 8.5  |
| 2023201777   | 许家淼 | 3      | 1     | 8.5  |
| 2023201778   | 顾梓民 | 1      | 1     | 8.5  |
| 2023201779   | 孙一丹 | 7      | 2     | /    |
| 2023201780   | 袁博辰 | 15     | 4     | 8    |
| 2023201781   | 王子涵 | 11     | 3     | 8.5  |
| 2023201782   | 柏欣妍 | 9      | 3     | 8.5  |




## Emphasis:

  - **!!Original work!!:** Plagiarism will not be tolerated.

- **Code Guide:** Refer to the Google Python Style Guide for elegant code writing

  - Chinese version: https://zh-google-styleguide.readthedocs.io/en/latest/google-python-styleguide/python_language_rules.html
  - English version: https://github.com/google/styleguide
  - Sargent Code: https://github.com/Quant-of-Renmin-University/QuantEcon2025_RUC/blob/main/Codes/A_QuantEcon_Sargent/15_writing_good_code.ipynb

## Appendix:

#### ***Appendix 1:***

*MLR.3: No Perfect Collinearity.

The assumption only requires that the independent variables should not have a perfect linear relationship. For example, variables with a relationship like: $x_1 + x_2 = x_3$.

Therefore, we need to remove one category (as the base category) in the regression.

[1] Wooldridge, Jeffrey M. *Introductory Econometrics: A Modern Approach* 6th ed. Cengage Learning, 2016.

<a id="appendix2"></a>

#### ***Appendix 2:***

In regression analysis, categorical variables need proper encoding for correct model inclusion. Directly assigning values like 1, 2, 3, 4 to a categorical variable can mislead the model into treating it as a numerical variable with order and interval relationships, leading to incorrect interpretations.

To avoid this issue, use methods like:

***OneHotEncoder***: Create binary dummy variables (0 or 1) for each category.
<a id="appendix3"></a>

#### ***Appendix 3:***

In order to generate images in python that can be displayed in Chinese, we need to add codes:

```Python
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用黑体显示中文
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
```



