from functions import extract_portaria_text, save_jsonl, clean_text
from pathlib import Path

if __name__ == "__main__":
    
    output_path_raw = "../data/raw/ministerio_saude/"
    Path(output_path_raw).mkdir(parents=True, exist_ok=True)
    output_path_trusted = "../data/trusted/ministerio_saude/ministerio_saude.jsonl"
    lst_ministerio_saude = []
    
    urls = [
        'https://bvsms.saude.gov.br/bvs/saudelegis/gm/2013/prt0529_01_04_2013.html',
        'https://bvsms.saude.gov.br/bvs/saudelegis/gm/2013/prt1377_09_07_2013.html',
        'https://bvsms.saude.gov.br/bvs/saudelegis/gm/2013/prt2095_24_09_2013.html',
        'https://bvsms.saude.gov.br/bvs/saudelegis/gm/2013/prt3390_30_12_2013.html',
        'https://bvsms.saude.gov.br/bvs/saudelegis/gm/2014/prt3410_30_12_2013.html',
        'https://bvsms.saude.gov.br/bvs/saudelegis/gm/2015/prt0285_24_03_2015.html',
        'https://bvsms.saude.gov.br/bvs/saudelegis/gm/2014/prt0389_13_03_2014.html',
        'https://bvsms.saude.gov.br/bvs/saudelegis/gm/2014/prt0183_30_01_2014.html'
        
    ]    
    
    for url in urls:
        
        # Read and save the text data in raw format
        
        raw_text = extract_portaria_text(url, output_path = f"{output_path_raw}{url[-23:-5]}.txt")
        
        text = clean_text(raw_text)
        
        # Save the data as jsonl format
        
        json_ministerio_saude_tmp = {
            "source": url,
            "category": "regulacao",
            "font": "ministerio_saude",
            "text": text
        }
        lst_ministerio_saude.append(json_ministerio_saude_tmp)

    save_jsonl(lst_ministerio_saude, output_path_trusted)
    print(f"✅ Arquivo salvo em: {output_path_trusted} ({len(lst_ministerio_saude)} documentos)")