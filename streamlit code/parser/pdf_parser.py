import os
from pdfminer.high_level import extract_text
from pdfminer.pdfparser import PDFSyntaxError


def extract_text_from_pdf(file_path):
    """
    Extract text from PDF file
    """
    try:
        if not os.path.exists(file_path):
            print("File not found:", file_path)
            return ""

        text = extract_text(file_path)

        if text:
            return text.strip()
        else:
            return ""

    except PDFSyntaxError:
        print("Invalid or corrupted PDF file")
        return ""

    except Exception as e:
        print("Error reading PDF:", e)
        return ""


def parse_pdf(file_path):
    """
    Main PDF parser function
    """
    return extract_text_from_pdf(file_path)


# Test function
if __name__ == "__main__":
    file = "uploads/resume.pdf"
    content = parse_pdf(file)
    print(content)