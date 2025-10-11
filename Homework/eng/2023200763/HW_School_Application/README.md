# Homework Feedback

The overall score of your work is 8/10.

## Advice
1. 在循环外调用了模板：the DocxTemplate object is created outside the loop, and render and save are called repeatedly inside the loop. This causes the template to be modified after the first rendering, so subsequent renderings are based on an already modified document rather than the original template. As a result, all generated files may contain identical or incorrect content. The template should be reloaded in each iteration (i.e., move doc = DocxTemplate("SOP_template.docx") inside the loop).
2. 导入包：All package imports can be placed together at the beginning of the code for better organization and readability.
3. 添加错误处理：It is recommended to add try-except to catch possible errors.

TA：Xue Jiayi
