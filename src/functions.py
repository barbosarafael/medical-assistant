import pdfplumber
from pathlib import Path
import json
import requests
from bs4 import BeautifulSoup
import re
import unicodedata

def listar_caminhos(pasta: str):
    """Lista todos os arquivos de uma pasta de forma recursiva."""
    p = Path(pasta)
    return [str(arquivo) for arquivo in p.rglob('*') if arquivo.is_file()]


def extract_clean_text(pdf_path: str) -> str:
    """Extrai e limpa o texto de um PDF."""
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text(x_tolerance=2, y_tolerance=2)
            if page_text:
                text += page_text + "\n\n"
    return text.strip()


def save_jsonl(data: list, output_path: str):
    """
    Salva uma lista de dicionários em formato JSONL.

    Args:
        data (list): lista de dicionários.
        output_path (str): caminho completo do arquivo .jsonl.
    """
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        for doc in data:
            json.dump(doc, f, ensure_ascii=False)
            f.write("\n")
            
            
def extract_portaria_text(url, output_path=None):
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"Erro ao acessar {url}: {e}")
        raise

    resp.encoding = resp.apparent_encoding
    html = resp.text

    soup = BeautifulSoup(html, "html.parser")

    main_div = soup.find("div", id="conteudo")
    if main_div is None:
        main_div = soup.body
        if main_div is None:
            raise RuntimeError("Não foi encontrado body nem div#conteudo")

    raw_text = main_div.get_text(separator="\n", strip=True)

    text = re.sub(r"\s{2,}", " ", raw_text)
    text = unicodedata.normalize("NFKC", text)
    text = ''.join(ch for ch in text if unicodedata.category(ch)[0] != "C")

    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Arquivo salvo em: {output_path}")

    return text

def clean_text(text: str) -> str:
    """
    Limpa e normaliza textos de diferentes fontes (PDF, HTML, CSV).
    
    Etapas:
    1. Normalização Unicode (NFKC)
    2. Remoção de caracteres de controle e não imprimíveis
    3. Substituição de múltiplos espaços, tabs e quebras de linha
    4. Remoção de caracteres redundantes como "�", "\x0c", etc.
    5. Padronização de aspas e traços
    6. Strip final e retorno
    
    Args:
        text (str): texto bruto extraído.
    
    Returns:
        str: texto limpo e normalizado.
    """

    if not text:
        return ""

    # 1. Normaliza para evitar variações Unicode (acentos compostos, etc.)
    text = unicodedata.normalize("NFKC", text)

    # 2. Remove caracteres de controle e não imprimíveis (C0/C1)
    text = ''.join(ch for ch in text if unicodedata.category(ch)[0] != "C")

    # 3. Remove caracteres substitutos corrompidos comuns em PDFs
    text = text.replace("�", "")

    # 4. Substitui múltiplos espaços, tabs e quebras de linha por um único espaço
    text = re.sub(r"[\r\t\f\v]+", " ", text)
    text = re.sub(r"\s{2,}", " ", text)

    # 5. Substitui traços e aspas tipográficas por versões simples
    text = text.replace("“", '"').replace("”", '"').replace("‘", "'").replace("’", "'")
    text = text.replace("–", "-").replace("—", "-")

    # 6. Remove espaços antes de pontuação
    text = re.sub(r"\s+([,.!?;:])", r"\1", text)

    # 7. Remove cabeçalhos de página comuns em PDFs (ex: “Página X de Y”)
    text = re.sub(r"Página\s+\d+\s+(de\s+\d+)?", "", text, flags=re.IGNORECASE)

    # 8. Remove múltiplas quebras de linha
    text = re.sub(r"\n{2,}", "\n", text)

    # 9. Trim final
    text = text.strip()

    return text
