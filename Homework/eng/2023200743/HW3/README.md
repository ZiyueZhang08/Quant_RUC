# Homework Feedback

The overall score of your work is 8/10.

## Advice
1. The code creates a DocxTemplate object outside the loop and repeatedly calls render and save inside the loop. This causes the template to be modified after the first rendering, so subsequent renderings are based on the modified document rather than the original template. As a result, all files may contain the same content or errors. The template should be reloaded in each iteration (move tpl = DocxTemplate(template_path) inside the loop).
2. Variable naming issue: print("输出目录：", os.path.abspath(OUTPUT_DIR)) should use output_dir (lowercase) according to the variable defined above.
3. Consider adding a try-except block for better error handling.

TA: Xue Jiayi
