import json
import chromadb
from chromadb.config import Settings
from chromadb import PersistentClient

# ==============================================
# CONFIGURAÇÕES
# ==============================================
EMBEDDINGS_PATH = "data/embeddings/vector_store.jsonl"
CHROMA_PATH = "data/vector_db"
COLLECTION_NAME = "medical_docs"

# ==============================================
# CARREGAR EMBEDDINGS DO JSONL
# ==============================================
def load_embeddings(path):
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            yield json.loads(line)

# ==============================================
# CONSTRUIR VECTOR STORE (Chroma)
# ==============================================
def main():
    print(f"[📦] Carregando embeddings de {EMBEDDINGS_PATH}...")
    data = list(load_embeddings(EMBEDDINGS_PATH))
    print(f"[✅] {len(data)} registros carregados.")

    client = PersistentClient(path=CHROMA_PATH)

    collection = client.get_or_create_collection(COLLECTION_NAME)

    print(f"[🚀] Inserindo embeddings no ChromaDB...")
    ids = [d["chunk_id"] for d in data]
    embeddings = [d["embedding"] for d in data]
    metadatas = [{"source": d["source"], "category": d["category"], "font": d["font"], "text": d["text"]} for d in data]
    
    print(metadatas)

    # Inserir em lotes para não travar memória
    batch_size = 500
    for i in range(0, len(data), batch_size):
        batch_ids = ids[i:i+batch_size]
        batch_embeddings = embeddings[i:i+batch_size]
        batch_metadata = metadatas[i:i+batch_size]

        collection.add(
            ids=batch_ids,
            embeddings=batch_embeddings,
            metadatas=batch_metadata,
            documents=[d["text"] for d in data[i:i+batch_size]]
        )
        print(f"✅ Inseridos: {i+len(batch_ids)}/{len(data)}")

    print(f"[💾] Vector store salvo em: {CHROMA_PATH}")

if __name__ == "__main__":
    main()
