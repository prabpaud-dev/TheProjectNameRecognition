import pymupdf
from pathlib import Path



def extract_text_from_pdf(doc):
    text = ""
    pdf = pymupdf.open(doc)

    for page in pdf:
        text += page.get_text()

    pdf.close()
    return text

def extract_pdf_dataset(dataset, pdfs_directory, suffix=""):
    results = []
    for record in dataset:

        document_id = record["id"]
        pdf_path = Path(pdfs_directory) / f"{document_id}{suffix}.pdf"
        if not pdf_path.exists():
            continue
        text = extract_text_from_pdf(pdf_path)

        results.append({
            "id": document_id,
            "text": text
        })
    return results