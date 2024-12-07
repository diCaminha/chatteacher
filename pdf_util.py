from PyPDF2 import PdfReader


def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = []
    for page in reader.pages:
        text.append(page.extract_text())
    return "\n".join(text)
