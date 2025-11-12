from pathlib import Path
import json
from text_utils import load_jsonl, chunk_text, count_tokens, log_info

def process_jsonl(input_path: str, output_path: str, max_tokens: int = 500):
    """
    Lê um arquivo .jsonl, divide cada texto em chunks e salva em novo arquivo.
    """
    docs = load_jsonl(input_path)
    chunked_docs = []

    for idx, doc in enumerate(docs):
        text = doc.get("text", "")
        if not text.strip():
            continue

        chunks = chunk_text(text, max_tokens=max_tokens)

        for i, chunk in enumerate(chunks):
            chunked_docs.append({
                "source": doc.get("source"),
                "category": doc.get("category"),
                "font": doc.get("font"),
                "chunk_id": f"{Path(input_path).stem}_{idx:03d}_{i:03d}",
                "text": chunk
            })

    # Salva no arquivo consolidado
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "a", encoding="utf-8") as f:
        for item in chunked_docs:
            json.dump(item, f, ensure_ascii=False)
            f.write("\n")

    log_info(f"✅ {Path(input_path).name} processado ({len(chunked_docs)} chunks gerados)")


if __name__ == "__main__":
    log_info("🚀 Iniciando o processo de chunking...")

    input_dir = Path("../data/trusted/")
    output_file = "../data/refined/chunked_docs.jsonl"
    Path(output_file).unlink(missing_ok=True)  # recria do zero

    jsonl_files = list(input_dir.rglob("*.jsonl"))
    if not jsonl_files:
        log_info("❌ Nenhum arquivo JSONL encontrado em data/trusted/")
        exit()

    total_tokens = 0
    for file in jsonl_files:
        docs = load_jsonl(file)
        for doc in docs:
            total_tokens += count_tokens(doc.get("text", ""))

    log_info(f"📊 Total estimado de tokens antes do chunking: {total_tokens:,}")

    for file in jsonl_files:
        process_jsonl(str(file), output_file, max_tokens=500)

    log_info(f"🏁 Chunking finalizado! Arquivo salvo em: {output_file}")
