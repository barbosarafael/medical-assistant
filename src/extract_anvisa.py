import pdfplumber
from pathlib import Path
import json

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
    
    lst_anvisa = []
    
    for file in caminhos:
        
        raw = extract_clean_text(file)
        category = 'regulacao'
        font = 'anvisa'
        
        json_anvisa_tmp = {
            'source': file,
            'category': category,
            'font': font,
            'text': raw
        }
        
        lst_anvisa.append(json_anvisa_tmp)
    
    with open("../data/trusted/anvisa.jsonl", "w", encoding="utf-8") as f:
        for doc in lst_anvisa:
            json.dump(doc, f, ensure_ascii=False)
            f.write("\n")