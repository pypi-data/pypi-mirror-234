import os

import pandas as pd
import glob
from fpdf import FPDF

WIDTH_COL = 20


def generate(invoices_paths, pdfs_path, img_path, product_id, product_name,
             amount_purchases, price_per_unit, total_price):
    """
    This function converts Excel invoices to pdf invoices
    :param invoices_paths:
    :param pdfs_path:
    :param img_path:
    :param product_id:
    :param product_name:
    :param amount_purchases:
    :param price_per_unit:
    :param total_price:
    :return:
    """
    os.makedirs(pdfs_path)
    for filepath in glob.glob(f"{invoices_paths}/*.xlsx"):

        df = pd.read_excel(filepath, sheet_name="Sheet 1")
        pdf = FPDF(orientation="P", unit="mm", format="A4")

        pdf.add_page()

        # Getting filename parsed
        pdf_filepath = filepath.replace(f"{invoices_paths}", f"{pdfs_path}")
        pdf_filepath = pdf_filepath.replace("xlsx", "pdf")
        pdf.set_font(family="Times", size=16, style="B")

        filename = filepath.strip("invoices/")
        filename = filename.strip(".xlsx")
        filename = filename.partition("-")
        # Creating Header
        pdf.cell(w=50, h=8, txt=f"Invoice number: {filename[0]}", ln=1)
        pdf.cell(w=50, h=8, txt=f"Invoice date: {filename[2]}", ln=1)
        pdf.ln(2)
        # Creating Index Row
        col = df.columns.to_list()
        for index, item in enumerate(col):
            col[index] = col[index].replace("_", " ")
            col[index] = col[index].title()

        pdf.set_font(family="Times", size=10, style="B")
        pdf.cell(w=20, h=8, txt=col[0], ln=0, border=1, align="C")
        pdf.cell(w=80, h=8, txt=col[1], ln=0, border=1, align="C")
        pdf.cell(w=40, h=8, txt=col[2], ln=0, border=1, align="C")
        pdf.cell(w=30, h=8, txt=col[3], ln=0, border=1, align="C")
        pdf.cell(w=20, h=8, txt=col[4], ln=1, border=1, align="C")

        # Creating Table Content, calculation total
        total_cost = 0.0
        for index, row in df.iterrows():
            pdf.cell(w=20, h=8, txt=str(row[product_id]), ln=0, border=1, align="L")
            pdf.cell(w=80, h=8, txt=str(row[product_name]), ln=0, border=1, align="L")
            pdf.cell(w=40, h=8, txt=str(row[amount_purchases]), ln=0, border=1, align="L")
            pdf.cell(w=30, h=8, txt=str(row[price_per_unit]), ln=0, border=1, align="L")
            pdf.cell(w=20, h=8, txt=str(row[total_price]), ln=1, border=1, align="L")
            total_cost = total_cost + float(row[total_price])

        # Creating Total Cost Row
        pdf.cell(w=20, h=8, txt="", ln=0, border=1, align="L")
        pdf.cell(w=80, h=8, txt="", ln=0, border=1, align="L")
        pdf.cell(w=40, h=8, txt="", ln=0, border=1, align="L")
        pdf.cell(w=30, h=8, txt="", ln=0, border=1, align="L")
        pdf.cell(w=20, h=8, txt=str(total_cost), ln=1, border=1, align="L")

        pdf.ln(25)
        pdf.set_font(family="Times", size=10, style="B")
        pdf.cell(w=20, h=8, txt=f"The total amount due is: {str(total_cost)} Euros.", ln=1, border=0, align="L")
        pdf.cell(w=20, h=8, txt="Pythonhow", ln=0, border=0, align="L")
        pdf.image(name=f"{img_path}", link="http://pythonhow.com", w=7, h=7)


        pdf.output(pdf_filepath)

if __name__ == "__main__":
    generate('invoices', 'test', 'pythonhow.png', 'product_id', 'product_name', 'amount_purchased', 'price_per_unit',
             'total_price')