import pandas as pd
from docxtpl import DocxTemplate
from docx2pdf import convert

desktop = r"C:\Users\Lenovo\Desktop"
template_path = desktop + r"\Word template.docx"
output_folder = desktop + r"\output_letters"
universities = pd.read_excel(desktop + r"\list_1 university.xlsx")
list2 = pd.read_excel(desktop + r"\list_2.xlsx")


for i in range(len(universities)):
    uni = str(universities.iloc[i, 0])  

    for j in range(len(list2)):
        research = str(list2.iloc[j, 0])
        top1 = str(list2.iloc[j, 1])
        top2 = str(list2.iloc[j, 2])
        top3 = str(list2.iloc[j, 3])
        skill = str(list2.iloc[j, 4])

        context = {
            'University': uni,
            'research': research,
            'top_jouranl_1': top1,
            'top_jouranl_2': top2,
            'top_jouranl_3': top3,
            'skill': skill
        }

        doc = DocxTemplate(template_path)
        doc.render(context)

        filename =f"{i+1:02d}_{uni}_{research}.docx"
        file_path = output_folder + "\\" + filename

        doc.save(file_path)

        try:
            convert(file_path)
        except Exception as e:
            print("sad：", e)

print("okk")
