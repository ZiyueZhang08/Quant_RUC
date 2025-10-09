import os
import pandas as pd
from docxtpl import DocxTemplate
from docx2pdf import convert

#生成申请信
def gen_appli(template_path, output_dir, university, field_info):    
    template = DocxTemplate(template_path)      #加载模板
    field = field_info['fields']
    journals = field_info['top journals']
    career_goal = field_info['Career goal']
    skills = field_info['skills']
    courses = field_info['courses I have taken']

    #填充模板（恶作剧GPA嘻嘻）
    context = {
        'Program_Name': 'Master of ' + field.capitalize(),
        'University_Name': university,
        'Field_of_Interest': field,
        'Relevant_Courses': courses,
        'GPA': '4.0 (top 5%)',
        'Journals':journals,
        'Career_Goal': career_goal,
        'Skills':skills
    }
    
    template.render(context)    
    output_docx = os.path.join(output_dir,f'{university}_{field}.docx')     #文件名
    output_pdf = os.path.join(output_dir,f'{university}_{field}.pdf')
    template.save(output_docx)
    convert(output_docx, output_pdf)

def main():
    #读取
    universities_df = pd.read_excel('university.xlsx')
    universities = universities_df['University Name'].tolist()      #加速
    other_info_df = pd.read_excel('other info.xlsx')    
    valid_rows = other_info_df[other_info_df['fields'].notna()]

    output_dir = 'HW_School_Application'        #输出目录
    os.makedirs(output_dir, exist_ok=True)      #创建目录

    for index, field_info in valid_rows.iterrows():      #按行迭代，不然只有列名QaQ
        #for university in ['Harvard University','MIT','UC Berkeley']:
        for university in (universities):
            gen_appli('demo.docx', output_dir, university, field_info)

    print("Finish!!!")


if __name__ == "__main__":
    main()