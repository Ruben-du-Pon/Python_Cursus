from fpdf import FPDF
import pandas as pd


def set_footer():
    pdf.set_font('Times', 'I', 8)
    pdf.set_text_color(180, 180, 180)
    pdf.cell(w=0, h=8, txt=row['Topic'], align='R', ln=1)


pdf = FPDF(orientation='P', unit='mm', format='A4')
pdf.set_auto_page_break(auto=False, margin=0)
df = pd.read_csv('topics.csv')


for index, row in df.iterrows():
    pdf.add_page()
    pdf.set_font('Times', 'B', 24)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(w=0, h=12, txt=row['Topic'], ln=1, align='L')
    pdf.line(10, 21, 200, 21)
    pdf.ln(263)
    set_footer()

    for _ in range(row['Pages']-1):
        pdf.add_page()
        pdf.ln(275)
        set_footer()
pdf.output('PDF_Template.pdf')
