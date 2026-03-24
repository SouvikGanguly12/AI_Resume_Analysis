import docx2txt
from pdfminer.high_level import extract_text
import os

def extract_text_from_docx(file_path):
    try:
        text = docx2txt.process(file_path)
        return text
    except Exception as e:
        print("Error reading DOCX:", e)
        return ""
    
def extract_text_from_pdf(file_path):
    try:
        text = extract_text(file_path)
        return text
    except Exception as e:
        print("Error reading PDF:", e)
        return ""
    
def parse_resume(file_path):
    if not os.path.exists(file_path):
        return ""
    if file_path.endswith(".docx"):
        return extract_text_from_docx(file_path)
    
    elif file_path.endswith(".pdf"):
        return extract_text_from_pdf(file_path)
    
    else:
        print("Unsupported file format")
        return ""