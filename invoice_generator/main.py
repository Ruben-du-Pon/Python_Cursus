import pandas as pd
import glob
from fpdf import FPDF
from pathlib import Path

filepaths = glob.glob("invoices/*.xlsx")


for filepath in filepaths:
    pdf = FPDF(orientation='P', unit='mm', format='A4')

    # Register fonts from the fonts directory
    pdf.add_font("FreeSerif", "", "fonts/FreeSerif.ttf", uni=True)
    pdf.add_font("FreeSerif", "B", "fonts/FreeSerifBold.ttf", uni=True)
    pdf.add_font("FreeSerif", "I", "fonts/FreeSerifItalic.ttf", uni=True)
    pdf.add_font("FreeSerif", "BI", "fonts/FreeSerifBoldItalic.ttf", uni=True)
    pdf.add_page()

    filename = Path(filepath).stem
    invoice_nr = filename.split("-")[0]
    date = filename.split("-")[1]
    date = date.replace(".", "/")

    pdf.set_font("FreeSerif", size=16, style='B')
    pdf.cell(w=50, h=8, txt=f"Invoice nr.: {invoice_nr}", ln=1)
    pdf.cell(w=50, h=8, txt=f"Date: {date}", ln=1)
    pdf.ln(5)

    df = pd.read_excel(filepath, sheet_name="Sheet 1")

    # Add table headers
    headers = list(df.columns)
    headers = [header.replace("_", " ").title() for header in headers]
    pdf.set_font("FreeSerif", size=10, style='B')
    pdf.cell(w=32, h=8, txt=headers[0], ln=0, border=1)
    pdf.cell(w=50, h=8, txt=headers[1], ln=0, border=1)
    pdf.cell(w=32, h=8, txt=headers[2], ln=0, border=1)
    pdf.cell(w=32, h=8, txt=headers[3], ln=0, border=1)
    pdf.cell(w=32, h=8, txt=headers[4], ln=1, border=1)

    # Add table rows
    for index, row in df.iterrows():
        pdf.set_font("FreeSerif", size=10)
        pdf.cell(w=32, h=8, txt=str(row["product_id"]), ln=0, border=1)
        pdf.cell(w=50, h=8, txt=str(row["product_name"]), ln=0, border=1)
        pdf.cell(w=32, h=8, txt=str(row["amount_purchased"]), ln=0, border=1)
        pdf.cell(w=32, h=8, txt=str(row["price_per_unit"]), ln=0, border=1)
        pdf.cell(w=32, h=8, txt=str(row["total_price"]), ln=1, border=1)

    # Calculate total price
    total_price = df["total_price"].sum()

    pdf.set_font("FreeSerif", size=10, style='B')
    pdf.cell(w=32, h=8, txt="Total:", ln=0, border=1)
    pdf.cell(w=50, h=8, txt="", ln=0, border=1)
    pdf.cell(w=32, h=8, txt="", ln=0, border=1)
    pdf.cell(w=32, h=8, txt="", ln=0, border=1)
    pdf.cell(w=32, h=8, txt=str(total_price), ln=1, border=1)

    pdf.ln(5)
    # Add total price to the end of the invoice
    pdf.set_font("FreeSerif", size=12, style='B')
    euro_sign = chr(8364)
    pdf.cell(
        w=0, h=8, txt=f"The total price is: {euro_sign}{total_price}", ln=1)

    # Add company information
    pdf.set_font("FreeSerif", size=10)
    pdf.cell(w=0, h=8, txt="Company name: Invoice Generator", ln=1)

    pdf.output(f"pdf_invoices/{filename}.pdf")

print("Files created succesfully!")
