

from pdfminer.high_level import extract_text
from docx import Document



def parse_pdf(file_path):
    try:
        text_data = extract_text(file_path)
        return text_data
    except Exception as e:
        print("PDF read karte waqt error aaya:", e)
        return ""



def parse_docx(file_path):
    try:
        document = Document(file_path)
        full_text = []

        
        for para in document.paragraphs:
            full_text.append(para.text)

        final_text = "\n".join(full_text)
        return final_text

    except Exception as e:
        print("DOCX read karte waqt error aaya:", e)
        return ""