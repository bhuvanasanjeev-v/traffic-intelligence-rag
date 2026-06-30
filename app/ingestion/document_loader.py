from docx import Document
import pandas as pd
from pypdf import PdfReader


def load_pdf(file_path):
    reader = PdfReader(file_path)

    text = ""

    for page in reader.pages:
        text += page.extract_text() + "\n"

    return text


def load_excel(file_path):
    sheets = pd.read_excel(
        file_path,
        sheet_name=None,
    )

    text = ""

    for sheet_name, df in sheets.items():
        text += f"\nSheet: {sheet_name}\n"
        text += df.to_string()

    return text


def load_docx(file_path):
    doc = Document(file_path)

    text = ""

    for para in doc.paragraphs:
        text += para.text + "\n"

    return text
