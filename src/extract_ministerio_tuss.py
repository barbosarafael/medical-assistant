import csv
import json
from pathlib import Path
from functions import clean_text

input_csv = "../data/raw/tuss/Tabela_20_Medicamentos.csv"
output_jsonl = "../data/trusted/tuss/tuss.jsonl"

Path(output_jsonl).parent.mkdir(parents=True, exist_ok=True)

with open(input_csv, encoding="utf-8") as f_in, open(output_jsonl, "w", encoding="utf-8") as f_out:
    reader = csv.DictReader(f_in, delimiter=";")  # troque para "," se for CSV americano
    for row in reader:
        # Cria texto concatenando as principais colunas
        raw = f"Código: {row.get('Código do Termo')} | Termo: {row.get('Termo')} | Apresentação: {row.get('Apresentação')}"
        
        text = clean_text(raw)
        
        doc = {
            "source": "https://dados.gov.br/dados/conjuntos-dados/terminologia-unificada-da-saude-suplementar-tuss",
            "category": "codificacao",
            "font": "tuss",
            "text": text
        }
        json.dump(doc, f_out, ensure_ascii=False)
        f_out.write("\n")

print(f"✅ Arquivo salvo em: {output_jsonl}")