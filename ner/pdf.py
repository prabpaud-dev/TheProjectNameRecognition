import pymupdf
from pathlib import Path



def extract_text_from_pdf(doc):

    text = ""
    path = Path.open(doc)
    pdf = pymupdf.open(path)
    for page in pdf:
        print(page)
        text+=page.get_text()
    return text

def extract_pdf_dataset(dataset,pdfs_directory):

    results = []
    for record in dataset:

        document_id = record["id"]
        pdf_path = Path(pdfs_directory/f"{document_id}.pdf")
        text = extract_text_from_pdf(pdf_path)

        results.append({
            "id": document_id,
            "text": text
        })
    return results