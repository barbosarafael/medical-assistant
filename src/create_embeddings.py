import json
import os
from tqdm import tqdm
from sentence_transformers import SentenceTransformer
import numpy as np
import torch

# =====================================================
# CONFIGURAÇÕES
# =====================================================
CHUNK_PATH = "data/refined/chunked_docs.jsonl"
OUTPUT_PATH = "data/embeddings/vector_store.jsonl"
MODEL_NAME = "paraphrase-MiniLM-L6-v2"
BATCH_SIZE = 8  # seguro para GPU com 6 GB (RTX 2060)

# =====================================================
# FUNÇÕES AUXILIARES
# =====================================================

def load_chunks(path: str):
    """Carrega todos os chunks do arquivo JSONL."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Arquivo {path} não encontrado.")
    
    chunks = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            try:
                chunk = json.loads(line)
                if chunk.get("text", "").strip():  # ignora vazios
                    chunks.append(chunk)
            except json.JSONDecodeError:
                continue
    return chunks


def save_embeddings(chunks, embeddings, output_path):
    """Salva embeddings incrementalmente em JSONL."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "a", encoding="utf-8") as f:
        for chunk, emb in zip(chunks, embeddings):
            entry = {
                "chunk_id": chunk.get("chunk_id"),
                "source": chunk.get("source"),
                "category": chunk.get("category"),
                "font": chunk.get("font"),
                "text": chunk.get("text", ""),
                "embedding": emb.tolist()
            }
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def get_device():
    """Detecta se há GPU disponível."""
    if torch.cuda.is_available():
        gpu_name = torch.cuda.get_device_name(0)
        print(f"🟩 GPU detectada: {gpu_name}")
        return "cuda"
    else:
        print("🟦 Usando CPU (nenhuma GPU detectada).")
        return "cpu"


# =====================================================
# PIPELINE PRINCIPAL
# =====================================================

def main():
    print(f"[🔍] Carregando chunks de {CHUNK_PATH}...")
    chunks = load_chunks(CHUNK_PATH)
    print(f"[✅] Total de chunks carregados: {len(chunks)}")

    if not chunks:
        print("⚠️ Nenhum chunk válido encontrado. Abortando.")
        return

    print(f"[🧠] Carregando modelo de embeddings: {MODEL_NAME}")
    device = get_device()
    model = SentenceTransformer(MODEL_NAME, device=device)

    total_chunks = len(chunks)
    processed = 0

    print(f"[🚀] Iniciando geração de embeddings ({total_chunks} chunks)...")

    for i in tqdm(range(0, total_chunks, BATCH_SIZE), desc="Gerando embeddings", unit="batch"):
        batch = chunks[i:i + BATCH_SIZE]
        texts = [c["text"] for c in batch]

        try:
            embeddings = model.encode(
                texts,
                batch_size=BATCH_SIZE,
                convert_to_numpy=True,
                show_progress_bar=False
            )
            save_embeddings(batch, embeddings, OUTPUT_PATH)
            processed += len(batch)
        except Exception as e:
            print(f"⚠️ Erro no batch {i // BATCH_SIZE}: {e}")
            continue

        if processed % 1000 == 0:
            print(f"[💾] Progresso salvo: {processed}/{total_chunks}")

    print(f"[🏁] Finalizado! Total processado: {processed}/{total_chunks}")
    print(f"[📁] Embeddings salvos em: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
