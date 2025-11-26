import textwrap
from chromadb import PersistentClient
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch


# ==============================================
# CONFIGURAÇÕES
# ==============================================
DB_PATH = "data/vector_db"
COLLECTION_NAME = "medical_docs"
MODEL_NAME = "microsoft/Phi-3-mini-4k-instruct"  # leve, rápido, ótimo para RAG
TOP_K = 8
DEVICE = "cpu"


# ==============================================
# FUNÇÕES AUXILIARES
# ==============================================

def load_llm(model_name: str):
    """
    Carrega modelo LLM local via Transformers.
    """
    print(f"🧠 Carregando modelo local: {model_name} ...")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float16 if DEVICE == "cuda" else torch.float32,
        device_map=DEVICE,
    )
    print("✅ Modelo carregado!")
    return tokenizer, model


def retrieve_context(query: str, top_k: int = TOP_K):
    """
    Busca chunks relevantes no ChromaDB.
    """
    client = PersistentClient(path=DB_PATH)
    collection = client.get_collection(COLLECTION_NAME)

    results = collection.query(
        query_texts=[query],
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )

    context_blocks = []
    for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
        block = f"[Fonte: {meta['font']} | Categoria: {meta['category']}]\n{doc}"
        context_blocks.append(block)

    context = "\n\n---\n\n".join(context_blocks)
    return context, results


def build_prompt(question: str, context: str) -> str:
    """
    Gera o prompt final para o LLM com injeção de contexto.
    """
    prompt = f"""
Você é um assistente que responde SOMENTE com base nas informações abaixo.
Não invente. Se não souber, diga 'Não encontrei essa informação nas fontes oficiais.'

### CONTEXTO
{context}

### PERGUNTA DO USUÁRIO
{question}

### RESPOSTA (baseada apenas no contexto acima):
"""
    return textwrap.dedent(prompt).strip()


def generate_answer(tokenizer, model, prompt: str) -> str:
    """
    Gera a resposta usando o LLM local.
    """
    inputs = tokenizer(prompt, return_tensors="pt").to(DEVICE)

    output = model.generate(
        **inputs,
        max_new_tokens=350,
        temperature=0.1,
        do_sample=True,
        pad_token_id=tokenizer.eos_token_id,
    )

    return tokenizer.decode(output[0], skip_special_tokens=True)

def rerank_results(results):
    """
    Reordena os resultados do Chroma usando:
    - similaridade vetorial
    - sinais simples de domínio
    SEM usar intenção explícita.
    """

    ranked = []

    for doc, meta, dist in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0]
    ):
        # Score base vindo do embedding
        score = 1 / (1 + dist)

        # Pequeno bônus se for codificação (TUSS é mais objetiva)
        if meta.get("category") == "codificacao":
            score += 0.15

        # Pequeno bônus se o texto tem formato claro de código
        if "Código:" in doc or "Código :" in doc:
            score += 0.10

        ranked.append((score, doc, meta))

    # Ordena do maior score para o menor
    ranked.sort(key=lambda x: x[0], reverse=True)
    return ranked


# ==============================================
# MODO PRINCIPAL
# ==============================================
def ask(question: str):
    tokenizer, model = load_llm(MODEL_NAME)

    print(f"\n🔍 Pergunta: {question}\n")

    context, results = retrieve_context(question, TOP_K)
    
    # >>> AQUI entra o re-rank <<<
    ranked = rerank_results(results)

    context_blocks = []
    for score, doc, meta in ranked[:3]:  # você controla quantos vão pro contexto
        block = f"[Fonte: {meta['font']} | Categoria: {meta['category']}]\n{doc}"
        context_blocks.append(block)

    context = "\n\n---\n\n".join(context_blocks)

    print("📚 Contexto re-rankeado:")
    print("-" * 80)
    print(context)
    print("-" * 80)

    prompt = build_prompt(question, context)
    answer = generate_answer(tokenizer, model, prompt)

    print("\n🤖 Resposta:")
    print(answer)


if __name__ == "__main__":
    # Exemplo de pergunta
    ask("Qual o código usado para a VACINA ADSORVIDA MENINGOCÓCICA C?")
