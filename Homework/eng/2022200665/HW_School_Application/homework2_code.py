
import pandas as pd
import os
from docxtpl import DocxTemplate

# 📁 获取桌面路径
desktop = os.path.join(os.path.expanduser("~"), "Desktop")

# 📄 定义文件路径
template_path = os.path.join(desktop, "template_application_letter.docx")
university_path = os.path.join(desktop, "university_list_econ.xlsx")
research_path = os.path.join(desktop, "research_area_journals_skill_needed.xlsx")

# 📊 读取 Excel 数据
universities = pd.read_excel(university_path, header=None)[0].dropna().tolist()
research_df = pd.read_excel(research_path)

# 📄 加载 Word 模板
template = DocxTemplate(template_path)

# ✅ 可选：打印检查
print(f"✅ 已读取大学数量：{len(universities)}")
print(f"✅ 已读取研究方向数量：{len(research_df)}")

# 📁 设置输出路径（桌面文件夹）
output_dir = os.path.join(desktop, "HW_School_Application")
os.makedirs(output_dir, exist_ok=True)

doc_count = 0  # 计数器

for uni in universities:
    for _, research in research_df.iterrows():
        context = {
            "university": uni,
            "research_area": research["research_area"],
            "journal_1": research["journal_1"],
            "journal_2": research["journal_2"],
            "journal_3": research["journal_3"],
            "skills_list": research.get("skills_list", "Python, Excel, Stata")
        }

        doc_count += 1
        filename = f"application_{doc_count:03d}_{uni}_{research['research_area']}.docx"
        save_path = os.path.join(output_dir, filename)
        template.render(context)
        template.save(save_path)

print(f"✅ 已成功生成 {doc_count} 份 Word 申请信，保存在：{output_dir}")

from docx2pdf import convert
import os

# 📁 定义输出文件夹路径
desktop = os.path.join(os.path.expanduser("~"), "Desktop")
output_dir = os.path.join(desktop, "HW_School_Application")

# 📄 执行转换
try:
    convert(output_dir)  # 自动将文件夹内所有 .docx 文件转为 .pdf
    print("✅ 所有 Word 文件已成功转换为 PDF")
except Exception as e:
    print("⚠️ PDF 转换失败，请确认你使用的是 Windows 且已安装 Microsoft Word")
    print(f"错误详情：{e}")
