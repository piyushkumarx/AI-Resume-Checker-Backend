from pdfminer.high_level import extract_text
from docx import Document
import re


def clean_text(text):

    text = text.lower()
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def parse_pdf(file_path):

    try:
        text = extract_text(file_path)
        return clean_text(text)

    except Exception as e:
        print("PDF error:", e)
        return ""


def parse_docx(file_path):

    try:

        doc = Document(file_path)

        text = []

        for para in doc.paragraphs:
            text.append(para.text)

        combined = "\n".join(text)

        return clean_text(combined)

    except Exception as e:
        print("DOCX error:", e)
        return ""