#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# main.py
import pandas as pd
from docxtpl import DocxTemplate
import os
from pathlib import Path

EXCEL_FILE_PATH = "C:/Users/25339/Desktop/pyhon/HW_School_Application/universities.xlsx"  
TEMPLATE_PATH = "C:/Users/25339/Desktop/pyhon/HW_School_Application/wordtemplate.docx"

def create_research_data():
    research_data = {
        'research_area': ['Finance', 'Economics', 'Management'],
        'journals': [
            'Review of Financial Studies, Journal of Finance, Management Science',
            'American Economic Review, Econometrica, Journal of Political Economy', 
            'Strategic Management Journal, Academy of Management Journal, Organization Science'
        ],
        'skills': [
            'Python, SQL, Financial Modeling, Risk Management',
            'Python, R, Econometrics, Statistical Analysis',
            'Python, PowerBI, Leadership, Strategic Planning'
        ]
    }
    return pd.DataFrame(research_data)

def read_universities_from_excel():
    universities_df = pd.read_excel(EXCEL_FILE_PATH)
    universities_list = []
    for col in universities_df.columns:
        universities_list.extend(universities_df[col].dropna().tolist())
    universities_list = [str(uni).strip() for uni in universities_list]
    return universities_list

def generate_sop():
    universities_list = read_universities_from_excel()
    research_df = create_research_data()
    
    output_dir = Path("HW_School_Application")
    output_dir.mkdir(exist_ok=True)
    
    generated_count = 0
    your_name = "Yang Shuhui"
    
    # 加载外部模板文件
    doc = DocxTemplate(TEMPLATE_PATH)
    
    for university in universities_list:
        for _, research_row in research_df.iterrows():
            context = {
                'name': your_name,
                'university': university,
                'program': 'Master of Finance',
                'research_area': research_row['research_area'],
                'journals': research_row['journals'],
                'skills': research_row['skills']
            }
            
            doc.render(context)
            
            safe_uni = university.replace(' ', '_').replace(',', '')[:15]
            safe_area = research_row['research_area']
            filename = f"SOP_{safe_uni}_{safe_area}.docx"
            output_path = output_dir / filename
            
            doc.save(output_path)
            generated_count += 1
            print(f"生成 {generated_count}/90: {filename}")
    
    print(f"完成! 生成 {generated_count} 份申请信")

def convert_to_pdf():
    try:
        from docx2pdf import convert
        output_dir = Path("HW_School_Application")
        convert(str(output_dir), str(output_dir))
        print("已转换为PDF")
    except:
        print("跳过PDF转换")

if __name__ == "__main__":
    print("开始生成90份申请信...")
    generate_sop()
    convert_to_pdf()
    print("任务完成!")


# In[ ]:




