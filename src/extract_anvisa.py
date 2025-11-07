from functions import listar_caminhos, extract_clean_text, save_jsonl

if __name__ == "__main__":
    input_path = "../data/raw/anvisa/"
    output_path = "../data/trusted/anvisa/anvisa.jsonl"

    caminhos = listar_caminhos(input_path)
    lst_anvisa = []

    for file in caminhos:
        raw = extract_clean_text(file)
        json_anvisa_tmp = {
            "source": file,
            "category": "regulacao",
            "font": "anvisa",
            "text": raw
        }
        lst_anvisa.append(json_anvisa_tmp)

    save_jsonl(lst_anvisa, output_path)
    print(f"✅ Arquivo salvo em: {output_path} ({len(lst_anvisa)} documentos)")