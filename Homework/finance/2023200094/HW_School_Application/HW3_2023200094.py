import pandas as pd
from docxtpl import DocxTemplate
import os
import platform

# 定义文件和目录
excel_path = "HW3_2023200094.xlsx" 
template_path = "HW3_2023200094.docx"
output_dir = "Generated_Application_Letters"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 加载数据
print(f"正在从 Excel 文件 '{excel_path}' 中加载数据...")
# 读取 Institution 工作表
df_institutions = pd.read_excel(excel_path, sheet_name="Institution") 
# 读取 Person 工作表
df_person = pd.read_excel(excel_path, sheet_name="Person")
print("数据加载成功！")

# 加载 Word 模板
print(f"正在加载 Word 模板: {template_path}")
doc = DocxTemplate(template_path)

# 循环并生成文档
print("开始批量生成申请信...")
total_generated = 0

for index, institution_row in df_institutions.iterrows():
    university_name = institution_row['Institution']

    for _, person_row in df_person.iterrows():
        research_area = person_row['Research Area']
        program_name = f"Master of {research_area.title()}"

        context = {
            'university_name': university_name,
            'program_name': program_name,
            'research_area': research_area,
            'journal1': person_row['Journal1'],
            'journal2': person_row['Journal2'],
            'journal3': person_row['Journal3'],
            'skill1': person_row['Skill1'],
            'skill2': person_row['Skill2'],
            'skill3': person_row['Skill3'],
        }

        doc.render(context)
        safe_uni_name = university_name.split(',')[0].replace(" ", "_").replace('"', '')
        safe_area_name = research_area.replace(" ", "_")
        output_path_docx = os.path.join(output_dir, f"{safe_uni_name}_{safe_area_name}.docx")
        doc.save(output_path_docx)
        total_generated += 1

print(f"\n任务完成！总共生成了 {total_generated} 份申请信，保存在 '{output_dir}' 文件夹中。")

# 转换为 PDF
if platform.system() == "Windows":
    print("\n检测到 Windows 系统，正在尝试将 DOCX 转换为 PDF...")
    try:
        from docx2pdf import convert
        convert(output_dir)
        print("✅ 所有 Word 文档已成功转换为 PDF！")
    except Exception as e:
        print(f"  - 转换为 PDF 失败。错误信息: {e}")