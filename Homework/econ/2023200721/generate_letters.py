import pandas as pd
from docxtpl import DocxTemplate
from pathlib import Path
import platform

def load_data():
    universities_df = pd.read_excel('application_data.xlsx', sheet_name='Universities')
    research_df = pd.read_excel('application_data.xlsx', sheet_name='Research Areas')
    skills_df = pd.read_excel('application_data.xlsx', sheet_name='Skills')

    universities = universities_df['University Name'].tolist()

    research_data = {}
    for _, row in research_df.iterrows():
        research_data[row['Research Area']] = {
            'journal_1': row['Journal 1'],
            'journal_2': row['Journal 2'],
            'journal_3': row['Journal 3']
        }

    skills = skills_df['Skills'].tolist()
    skills_str = ', '.join(skills[:-1]) + ' and ' + skills[-1]

    return universities, research_data, skills_str

def generate_letters(student_name="Lei Ge", career_goal="quantitative researcher", convert_to_pdf=False):
    universities, research_data, skills_str = load_data()

    output_dir = Path('generated_letters')
    output_dir.mkdir(exist_ok=True)

    template = DocxTemplate('application_letter_template.docx')

    count = 0
    is_windows = platform.system() == 'Windows'

    if convert_to_pdf and not is_windows:
        print("Warning: PDF conversion is only supported on Windows. Generating Word files only.")
        convert_to_pdf = False

    if convert_to_pdf and is_windows:
        try:
            from docx2pdf import convert
            pdf_supported = True
        except ImportError:
            print("Warning: docx2pdf not installed. Run 'pip install docx2pdf' to enable PDF conversion.")
            pdf_supported = False
            convert_to_pdf = False

    for university in universities:
        for research_area, journals in research_data.items():
            context = {
                'student_name': student_name,
                'university_name': university,
                'research_area': research_area,
                'journal_1': journals['journal_1'],
                'journal_2': journals['journal_2'],
                'journal_3': journals['journal_3'],
                'career_goal': career_goal,
                'skills': skills_str
            }

            template.render(context)

            safe_uni_name = university.replace('/', '-').replace(' ', '_')
            safe_area_name = research_area.replace(' ', '_')
            filename = f"{safe_uni_name}_{safe_area_name}.docx"

            output_path = output_dir / filename
            template.save(str(output_path))

            if convert_to_pdf and pdf_supported:
                pdf_filename = filename.replace('.docx', '.pdf')
                pdf_path = output_dir / pdf_filename
                convert(str(output_path), str(pdf_path))

            count += 1

            template = DocxTemplate('application_letter_template.docx')

    return count, output_dir

def main():
    print("=" * 60)
    print("University Applications Letters Generator")
    print("=" * 60)

    print("\nPlease enter your personal information (press Enter for default):")
    student_name = input("Student Name (default: Lei Ge): ").strip()
    if not student_name:
        student_name = "Lei Ge"

    career_goal = input("Career Goal (default: quantitative researcher): ").strip()
    if not career_goal:
        career_goal = "quantitative researcher"

    convert_to_pdf = False
    if platform.system() == 'Windows':
        pdf_choice = input("Convert to PDF? (y/n, default: n): ").strip().lower()
        if pdf_choice == 'y':
            convert_to_pdf = True

    print(f"\nGenerating application letters...")
    print(f"Student Name: {student_name}")
    print(f"Career Goal: {career_goal}")
    if convert_to_pdf:
        print(f"Output Format: Word + PDF")
    else:
        print(f"Output Format: Word only")

    try:
        count, output_dir = generate_letters(student_name, career_goal, convert_to_pdf)

        print("\n" + "=" * 60)
        print(f"Successfully generated {count} application letters!")
        print(f"Files saved in: {output_dir.absolute()}")
        print("=" * 60)

        print(f"\nGeneration Statistics:")
        print(f"  - Number of Universities: 30")
        print(f"  - Research Areas: 3 (Economics, Finance, Management)")
        print(f"  - Total Files: {count}")

    except Exception as e:
        print(f"\nError occurred during generation: {e}")
        raise

if __name__ == "__main__":
    main()
