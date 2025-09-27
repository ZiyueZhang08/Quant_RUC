from docxtpl import DocxTemplate
import pandas as pd
import os
from docx2pdf import convert
import sys

def generate_application_letters():
    """
    生成90封研究生申请信
    """
    try:
        # 读取Excel数据
        df_universities = pd.read_excel(r"C:\Users\陈\Desktop\HW3\HW3.xlsx", sheet_name='Institution')
        df_research_areas = pd.read_excel(r"C:\Users\陈\Desktop\HW3\HW3.xlsx", sheet_name='Person')
        
        # 检查数据
        print(f"找到 {len(df_universities)} 所大学")
        print(f"找到 {len(df_research_areas)} 个研究领域")
        
        # 加载模板
        doc = DocxTemplate(r"C:\Users\陈\Desktop\HW3\template.docx")
        print("模板加载成功")
        
        # 创建输出目录
        output_dir = os.path.expanduser(r"C:\Users\陈\Desktop\HW3/HW_School_Application")
        word_dir = os.path.join(output_dir, "Word_Files")
        pdf_dir = os.path.join(output_dir, "PDF_Files")
        
        os.makedirs(word_dir, exist_ok=True)
        os.makedirs(pdf_dir, exist_ok=True)
        
        # 生成申请信
        count = 0
        generated_files = []
        
        for _, uni_row in df_universities.iterrows():
            for _, area_row in df_research_areas.iterrows():
                # 准备上下文数据
                context = {
                    'university_name': uni_row['Institution'],
                    'research_area': area_row['Research Area'],
                    'journal1': area_row['Journal1'],
                    'journal2': area_row['Journal2'],
                    'journal3': area_row['Journal3'],
                    'skill1': area_row['Skill1'],
                    'skill2': area_row['Skill2'],
                    'skill3': area_row['Skill3'],
                    'program_name': area_row['Research Area'].title()  # 首字母大写
                }
                
                # 生成文件名（移除特殊字符）
                safe_uni_name = "".join(c for c in uni_row['Institution'] if c.isalnum() or c in (' ', '-', '_')).rstrip()
                safe_area_name = "".join(c for c in area_row['Research Area'] if c.isalnum() or c in (' ', '-', '_')).rstrip()
                
                # 保存Word文档
                word_filename = f"Application_{count+1:02d}_{safe_uni_name.replace(' ', '_')}_{safe_area_name.replace(' ', '_')}.docx"
                word_path = os.path.join(word_dir, word_filename)
                
                doc.render(context)
                doc.save(word_path)
                generated_files.append(word_path)
                count += 1
                
                print(f"生成: {word_filename}")
        
        print(f"\n成功生成 {count} 封申请信")
        
        # 转换为PDF（仅Windows系统）
        if sys.platform == "win32":
            print("开始转换为PDF...")
            for word_file in generated_files:
                pdf_file = word_file.replace('Word_Files', 'PDF_Files').replace('.docx', '.pdf')
                try:
                    convert(word_file, pdf_file)
                    print(f"转换为PDF: {os.path.basename(pdf_file)}")
                except Exception as e:
                    print(f"转换失败 {word_file}: {e}")
            print("PDF转换完成")
        else:
            print("非Windows系统，跳过PDF转换")
        
        # 复制一份示例文件到根目录
        if generated_files:
            import shutil
            sample_file = generated_files[0]
            shutil.copy2(sample_file, os.path.join(output_dir, "Sample_Application.docx"))
            print(f"\n示例文件已保存至: {os.path.join(output_dir, 'Sample_Application.docx')}")
        
        return True
        
    except Exception as e:
        print(f"生成过程中出现错误: {e}")
        return False

def main():
    """
    主函数
    """
    print("开始生成研究生申请信...")
    print("=" * 50)
    
    success = generate_application_letters()
    
    if success:
        print("\n" + "=" * 50)
        print("任务完成！")
        print(f"文件保存在: {os.path.expanduser('~/HW_School_Application')}")
    else:
        print("\n生成失败，请检查错误信息")

if __name__ == "__main__":
    main()