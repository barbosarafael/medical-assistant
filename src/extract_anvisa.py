import pdfplumber
from pathlib import Path

def listar_caminhos(pasta: str):
    p = Path(pasta)
    caminhos = [str(arquivo) for arquivo in p.rglob('*')]  # rglob('*') = recursivo
    return caminhos

def extract_clean_text(pdf_path: str) -> str:
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text(x_tolerance=2, y_tolerance=2)
            if page_text:
                text += page_text + "\n\n"
    return text.strip()

if __name__ == "__main__":
    caminhos = listar_caminhos("../data/raw/anvisa/")
    
    for caminho in caminhos:
    
        pdf_path = "../data/raw/anvisa/Nota técnica n° 34.pdf"

        raw = extract_clean_text(pdf_path)

        print(raw[:1000])
