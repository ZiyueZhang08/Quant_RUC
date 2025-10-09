import os
import pandas as pd
from docxtpl import DocxTemplate
from docx2pdf import convert

def load_data(university_file, info_file):
    """
    读取表格    
    Args:
        university_file: 大学名称表的文件路径 (str)
        info_file: 专业信息的文件路径 (str)
    Returns:
        tuple[list, pd.DataFrame]: (大学名称列表, 含申请信息的数据框)
    """
    # 读取大学名单
    universities_df = pd.read_excel(university_file, header=None)
    universities = universities_df.iloc[:, 0].dropna().tolist()

    # 读取申请信息
    info_df = pd.read_excel(info_file)
    valid_rows = info_df[info_df['fields'].notna()]

    return universities, valid_rows


# 生成申请信
def gen_application(template_path, output_dir, university, field_info):
    """
    生成申请信
    Args:
        template_path: 模板文件路径 (str)
        output_dir: 输出目录 (str)
        university: 大学名称 (str)
        field_info: 包含申请信息的行数据 (pd.Series)
    """
    try:
        template = DocxTemplate(template_path)

        # 提取字段信息
        field = field_info['fields']
        journals = field_info['top journals']
        career_goal = field_info['Career goal']
        skills = field_info['skills']
        courses = field_info['courses I have taken']

        # 渲染上下文
        context = {
            'Program_Name': f"Master of {field.capitalize()}",
            'University_Name': university,
            'Field_of_Interest': field,
            'Relevant_Courses': courses,
            'Journals': journals,
            'Career_Goal': career_goal,
            'Skills': skills
        }

        # 渲染并保存临时文件
        temp_docx = os.path.join(output_dir, f"{university}_{field}.docx")
        output_pdf = os.path.join(output_dir, f"{university}_{field}.pdf")

        template.render(context)
        template.save(temp_docx)

        # 转换为PDF,删除word
        convert(temp_docx, output_pdf)
        if os.path.exists(temp_docx):
            os.remove(temp_docx)

    except Exception as e:
        print(f"生成 {university} 的申请信时出错: {e}")

def main():
    # 路径设置
    template_path = 'demo.docx'
    university_file = 'university.xlsx'
    info_file = 'other info.xlsx'
    output_dir = 'HW_School_Application'

    # 读数据
    universities, valid_rows = load_data(university_file, info_file)

    # 输出目录
    os.makedirs(output_dir, exist_ok=True)

    # 生成申请信
    for temp, field_info in valid_rows.iterrows():
        for university in universities:
            gen_application(template_path, output_dir, university, field_info)

    print("Finish!!!")

    # # 测试
    # test_universities = universities[:3]
    # for temp, field_info in valid_rows.iterrows():
    #     for university in test_universities:
    #         gen_application(template_path, output_dir, university, field_info)
    

if __name__ == "__main__":
    main()