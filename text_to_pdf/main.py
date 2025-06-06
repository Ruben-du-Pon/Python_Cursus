import glob
from fpdf import FPDF
from pathlib import Path

filepaths = glob.glob("txt_files/*.txt")

pdf = FPDF(orientation='P', unit='mm', format='A4')

for filepath in filepaths:
    pdf.add_page()

    animal = Path(filepath).stem.title()

    pdf.set_font("Times", size=16, style='B')
    pdf.cell(w=50, h=8, txt=animal, ln=1)

    with open(filepath, "r") as file:
        content = file.read()

    pdf.set_font("Times", size=12)
    pdf.multi_cell(w=0, h=6, txt=content)

pdf.output("pdf_files/animals.pdf")
