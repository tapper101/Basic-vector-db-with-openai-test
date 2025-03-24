# doc_loader.py
#from PyPDF2 import PdfReader
from pypdf import PdfReader
import docx
from bs4 import BeautifulSoup
import openpyxl

def load_pdf(path):
    reader = PdfReader(path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def load_docx(path):
    doc = docx.Document(path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

def load_txt(path):
    with open(path, "r", encoding="utf-8") as file:
        return file.read()

def load_html(path):
    with open(path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")
        return soup.get_text(separator="\n")

def load_excel(path):
    workbook = openpyxl.load_workbook(path)
    sheet = workbook.active

    rows = list(sheet.iter_rows(values_only=True))
    header = rows[0]  # Assumes first row is header
    data_rows = rows[1:]  # Exclude header

    return header, data_rows

def chunk_excel_rows(header, data_rows):
    chunks = []
    metadatas = []

    for idx, row in enumerate(data_rows):
        metadata = {f"col_{header[i]}": row[i] for i in range(min(7, len(row)))}
        content_cells = row[7:] if len(row) > 7 else []
        content = " | ".join(str(cell) for cell in content_cells if cell is not None)

        chunks.append(content if content else "No content")
        metadatas.append(metadata)

    return chunks, metadatas

def load_document(path):
    if path.endswith(".pdf"):
        return load_pdf(path)
    elif path.endswith(".docx"):
        return load_docx(path)
    elif path.endswith(".html") or path.endswith(".htm"):
        return load_html(path)
    elif path.endswith(".txt"):
        return load_txt(path)
    elif path.endswith(".xlsx"):
        header, data_rows = load_excel(path)
        return chunk_excel_rows(header, data_rows)
    else:
        raise ValueError("Unsupported file format")
