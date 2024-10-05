from PyPDF2 import PdfReader
from docx import Document

def handle_file_upload(uploaded_file):
    if uploaded_file.type == "text/plain":
        content = uploaded_file.read().decode("utf-8")
    elif uploaded_file.type == "application/pdf":
        reader = PdfReader(uploaded_file)
        content = ""
        for page in reader.pages:
            content += page.extract_text() or ""
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = Document(uploaded_file)
        content = "\n".join([para.text for para in doc.paragraphs])
    else:
        content = "Unsupported file type."
    return content
