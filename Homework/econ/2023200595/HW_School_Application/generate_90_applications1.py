import pandas as pd
from pathlib import Path
import time


def create_excel_files():
    """创建两个Excel数据文件"""
    base_path = Path(r"E:\Downloads\HW_School_Application")
    base_path.mkdir(parents=True, exist_ok=True)

    # 专业数据
    fields_data = {
        'Field': ['Economics', 'Management', 'Finance'],
        'Journals': [
            'American Economic Review; Quarterly Journal of Economics; Econometrica',
            'Management Science; Academy of Management Journal; Strategic Management Journal',
            'Journal of Finance; Review of Financial Studies; Journal of Financial Economics'
        ],
        'Skills': [
            'Econometrics; Causal Inference; Python; R; Stata; Data Analysis',
            'Organizational Behavior; Statistical Analysis; Survey Design; Excel; Python; Structural Equation Modeling',
            'Asset Pricing; Time Series Analysis; MATLAB; Python; SQL; Machine Learning'
        ]
    }

    fields_df = pd.DataFrame(fields_data)
    fields_file = base_path / "fields_journals_skills.xlsx"
    fields_df.to_excel(fields_file, index=False)
    print(f"已创建文件: {fields_file}")

    # 大学数据
    universities_list = [
        'Harvard University', 'Massachusetts Institute of Technology (MIT)', 
        'University of California, Berkeley', 'University of Chicago', 
        'Paris School of Economics', 'Princeton University', 'Stanford University',
        'Yale University', 'Toulouse School of Economics (TSE)', 'University of Oxford', 
        'Columbia University', 'University of Cambridge', 'Boston College', 
        'University of Toronto', 'University of Warwick', 'Cornell University', 
        'University of California, Davis', 'Rijksuniversiteit Groningen',
        'Johns Hopkins University', 'Università di Bologna', 'Sciences Po', 
        'University of Nottingham', 'University of California, Irvine (UCI)', 
        'Monash University', 'KU Leuven', 'Aarhus University',
        'University of Maryland, College Park', 'University of Southern California (USC)', 
        'Duke University', 'Michigan State University'
    ]

    universities_df = pd.DataFrame({'University': universities_list})
    universities_file = base_path / "universities_30.xlsx"
    universities_df.to_excel(universities_file, index=False)
    print(f"已创建文件: {universities_file}")

    return base_path, fields_df, universities_df


def convert_to_pdf_safe(generated_files):
    #安全的PDF转换函数，包含重试机制
    try:
        from docx2pdf import convert
    except ImportError:
        print("docx2pdf 未安装，跳过PDF转换")
        return 0
    
    print("开始转换PDF格式")
    pdf_count = 0
    failed_files = []
    
    for word_file in generated_files:
        max_retries = 3
        
        for attempt in range(max_retries):
            try:
                pdf_file = word_file.with_suffix('.pdf')
                
                # 如果PDF文件已存在，先删除
                if pdf_file.exists():
                    pdf_file.unlink()
                
                # 重试时添加延迟
                if attempt > 0:
                    time.sleep(2)
                
                convert(str(word_file), str(pdf_file))
                
                # 验证PDF文件是否成功创建
                if pdf_file.exists() and pdf_file.stat().st_size > 0:
                    pdf_count += 1
                    print(f"已转换: {word_file.name}")
                    break
                else:
                    print(f"转换失败: {word_file.name} (文件为空)")
                    failed_files.append(word_file.name)
                    break
                    
            except Exception as e:
                print(f" 转换失败 {word_file.name} (尝试 {attempt + 1}/{max_retries}): {e}")
                if attempt == max_retries - 1:
                    failed_files.append(word_file.name)
                time.sleep(1)
    
    # 输出转换结果
    print(f"\n转换完成: {pdf_count}/{len(generated_files)} 个文件成功转换")
    
    if failed_files:
        print(f"失败文件: {len(failed_files)} 个")
        for failed in failed_files[:5]:
            print(f"  - {failed}")
        if len(failed_files) > 5:
            print(f"  还有 {len(failed_files) - 5} 个失败文件")
    
    return pdf_count


def generate_application_documents(base_path, fields_df, universities_df):
    #生成申请文档并转换为PDF
    universities_list = universities_df["University"].tolist()
    
    personal_info = {
        "name": "Gaofu Yu",
        "program": "Master of Finance",
        "research_goal": "to become a quantitative researcher focusing on asset pricing and the application of data science",
        "why_university": "its strong research faculty and rigorous quantitative curriculum"
    }
    
    output_dir = base_path / "generated_applications"
    output_dir.mkdir(parents=True, exist_ok=True)

    from docxtpl import DocxTemplate

    count = 0
    generated_files = []
    template_file = base_path / "application_template.docx"
    template = DocxTemplate(template_file)
    
    for university in universities_list:
        for _, field_row in fields_df.iterrows():
            count += 1
            specific_interest = (
                f"the empirical analysis of {field_row['Field'].lower()} "
                f"with a focus on policy implications"
            )
            
            context = {
                "name": personal_info["name"],
                "program": personal_info["program"],
                "university": university,
                "field": field_row["Field"],
                "journals": field_row["Journals"],
                "skills": field_row["Skills"],
                "research_interest_specific": specific_interest,
                "research_goal": personal_info["research_goal"],
                "why_university": personal_info["why_university"]
            }
            
            template.render(context)
            
            # 生成文件
            safe_university = university.replace(' ', '_').replace('/', '_').replace(',', '')
            safe_field = field_row['Field'].replace(' ', '_')
            output_filename = output_dir / f"application_{count:03d}_{safe_university}_{safe_field}.docx"
            
            template.save(output_filename)
            generated_files.append(output_filename)

    pdf_count = convert_to_pdf_safe(generated_files)

    print(f"   生成文档数量: {count}")
    print(f"   PDF转换成功: {pdf_count}/{count}")
    print(f"  保存位置: {output_dir}")


def main():
    #主函数
    print("开始文档生成程序")
    print("=" * 50)
    
    base_path, fields_df, universities_df = create_excel_files()
    generate_application_documents(base_path, fields_df, universities_df)
    
    print("=" * 50)
    print("所有任务已完成")


if __name__ == "__main__":
    main()