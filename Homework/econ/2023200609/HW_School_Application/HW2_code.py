import pandas as pd
from docxtpl import DocxTemplate 
from docx2pdf import convert

import os  

# 读取第一个xlsx文件
df_universities = pd.read_excel('universities.xlsx')
universities_list = df_universities['university_name'].tolist()  
print(f"成功读取 {len(universities_list)} 所大学")

#读取第二个xlsx文档
df_majors = pd.read_excel('major.xlsx')
print("专业数据列名:", df_majors.columns.tolist())  # 显示所有列名

#加载word模板
template = DocxTemplate("sop_template.docx")

#遍历
count = 0  

for university in universities_list:
    for index, row in df_majors.iterrows():
        major = row['major']
        journal1 = row['top_journals_1']
        journal2 = row['top_journals_2']
        journal3 = row['top_journals_3']
        skills = row['skills']
        
        # 合并期刊
        journals = f"{journal1}, {journal2}, {journal3}"
        
        # 生成项目名称
        program_name = f"Master of {major} program"
        
        # 替换到模板
        context = {
            'university_name': university,
            'program_name': program_name,
            'journal_list': journals,
            'skill_list': skills,
        }
        
        filename = f"SOP_{university}_{program_name}.docx"
        file_path = os.path.join("SOP_word", filename)
        
        template.render(context)
        template.save(file_path)
        
        count += 1
        print(f"已生成第 {count} 份: {filename}")

print(f"\n成功生成 {count} 份申请信")
#转换为pdf文档
input_folder = "./SOP_word/"  
convert("SOP_word", "SOP_pdf")  