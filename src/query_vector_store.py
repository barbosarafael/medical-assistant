from chromadb import PersistentClient
import textwrap

# ==============================================
# CONFIG
# ==============================================
DB_PATH = "data/vector_db"
COLLECTION_NAME = "medical_docs"
QUERY = "Qual a regulamentação para produtos saneantes com ação anmicrobiana?"
TOP_K = 5

# ==============================================
# CONECTAR AO CHROMA
# ==============================================
client = PersistentClient(path=DB_PATH)
collection = client.get_collection(COLLECTION_NAME)

count = collection.count()
print(f"\n📦 Base carregada: {count} embeddings disponíveis.\n")

# ==============================================
# CONSULTA
# ==============================================
print(f"🔍 Consulta: {QUERY}\n")

results = collection.query(
    query_texts=[QUERY],
    n_results=TOP_K,
    include=["metadatas", "documents", "distances"]
)

# ==============================================
# EXIBIÇÃO FORMATADA
# ==============================================
if not results or not results.get("metadatas"):
    print("⚠️ Nenhum resultado encontrado.")
else:
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]
    documents = results.get("documents", [[]])[0]

    for i, meta in enumerate(metadatas):
        dist = distances[i]
        score = 1 / (1 + dist)  # converte distância em algo de 0–1
        print(f"🔹 Resultado {i+1} (score={score:.4f}):")
        print(f"   🏷️ Categoria: {meta.get('category')}")
        print(f"   🗂️ Fonte: {meta.get('font')}")
        print(f"   🌐 Source: {meta.get('source')}\n")
        print(f"   📄 Trecho: {documents[i]}\n")

        
        print("-" * 120)
