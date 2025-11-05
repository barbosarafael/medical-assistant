import pdfplumber
from pathlib import Path

def listar_caminhos(pasta: str):
    """Lista todos os arquivos e subpastas recursivamente."""
    p = Path(pasta)
    caminhos = [str(arquivo) for arquivo in p.rglob('*')]
    return caminhos


def extract_clean_text(pdf_path: str, output_path: str = None) -> str:
    """
    Extrai e limpa o texto de um PDF.
    Se 'output_path' for informado, salva o conteúdo em um arquivo .txt.
    """
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text(x_tolerance=2, y_tolerance=2)
            if page_text:
                text += page_text + "\n\n"

    text = text.strip()

    # 🔹 Se o output_path foi informado, salva o texto
    if output_path:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)  # cria diretórios se não existirem
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(text)

    return text


if __name__ == "__main__":
    input_dir = Path("../data/raw/anvisa/")
    output_dir = Path("../data/trusted/anvisa/")

    for caminho in listar_caminhos(input_dir):
        if caminho.endswith(".pdf"):
            pdf_path = Path(caminho)
            txt_name = pdf_path.stem + ".txt"  # mesmo nome, mas extensão .txt
            output_path = output_dir / txt_name

            texto = extract_clean_text(pdf_path, output_path=output_path)
            print(f"✅ Extraído e salvo: {output_path}")
