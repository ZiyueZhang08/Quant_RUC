from docxtpl import DocxTemplate
import pandas as pd
from pathlib import Path
from docx2pdf import convert

# Tips for using this script:
# 1. Write some comments in the code for better understanding.
# 2. The `safe_university` should be processed in the outter loop to 
#    avoid redundant processing. (In this code, each university will 
#    be processed `len(info_df)` times, which is inefficient.)

def generate_sop_documents():
    output_dir = Path("HW_School_Application")
    output_dir.mkdir(exist_ok=True)

    universities_df = pd.read_excel('university.xlsx')
    universities = universities_df['university'].tolist()
    info_df = pd.read_excel('information.xlsx')

    template = DocxTemplate("template.docx")

    document_count = 0
    first_doc = None

    for university in universities:
        for _, row in info_df.iterrows():
            context = {
                'university': university.strip(),
                'area': row['area'],
                'career': row['career'],
                'skill_1': row['skill_1'],
                'skill_2': row['skill_2'],
                'skill_3': row['skill_3'],
                'journal_1': row['journal_1'],
                'journal_2': row['journal_2'],
                'journal_3': row['journal_3']
            }

            safe_university = "".join(c for c in university if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_area = row['area']
            filename = f"{safe_university}_{safe_area}_SOP.docx"
            filepath = output_dir / filename

            template.render(context)
            template.save(filepath)
            document_count += 1

            if first_doc is None:
                first_doc = filepath

    # 转换第一个文档为PDF
    if first_doc:
        pdf_path = first_doc.with_suffix('.pdf')
        convert(first_doc, pdf_path)

if __name__ == "__main__":

    generate_sop_documents()
