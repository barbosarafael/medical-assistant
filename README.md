# 🩺 Assistente Médico Regulatório 🩺

> Assistente conversacional baseado em **LLM + RAG (Retrieval-Augmented Generation)** que responde perguntas sobre **regulação, normas, auditoria e codificação médica** utilizando apenas **fontes oficiais** (ANVISA, Ministério da Saúde e TUSS).  
> O projeto é **educacional** e visa explorar o ciclo completo de um sistema GenAI seguro e rastreável — sem emitir diagnósticos, prescrições ou recomendações clínicas.

## 🎯 Objetivo
Tem como missão facilitar o acesso a informações **regulatórias e administrativas** do setor de saúde brasileiro, centralizando dados dispersos e complexos em um ambiente de consulta natural.

---

## Escopos e Focos do Projeto

### **Regulação, Normas e Processos**
> Consulta e explicação de leis, portarias e resoluções oficiais.
- Ex: “O que diz a RDC 344/1998 da ANVISA?”
- Fontes: ANVISA, Ministério da Saúde e TUSS

--- 

## ⚙️ Arquitetura do Pipeline

```
📂 data/
├── raw/ # Dados brutos extraídos (PDF, CSV, HTML)
├── trusted/ # Dados convertidos e limpos (JSONL)
├── refined/ # Textos segmentados (chunks)
├── embeddings/ # Vetores gerados via SentenceTransformer
└── vector_db/ # Base vetorial persistida (Chroma)
```

---

## 🧩 Etapas do Pipeline

| Etapa | Script | Descrição |
|-------|--------|-----------|
| 1️⃣ Extração | `extract_anvisa.py`, `extract_ministerio_saude.py`, `extract_ministerio_tuss.py` | Captura textos brutos e salva em JSONL limpo |
| 2️⃣ Limpeza | `text_utils.py` | Normaliza texto, remove caracteres inválidos e organiza estrutura |
| 3️⃣ Chunking | `chunk_texts.py` | Divide textos em segmentos (~500 tokens) para melhor embedding |
| 4️⃣ Embeddings | `create_embeddings.py` | Gera embeddings com `SentenceTransformer` (MiniLM-L6-v2) |
| 5️⃣ Vector Store | `build_vector_store.py` | Persiste embeddings no **ChromaDB** com metadados completos |
| 6️⃣ Consulta | `query_vector_store.py` | Permite buscas semânticas com score de relevância e fonte |

---

## 🧱 Estrutura do Repositório

```
src/
├── build_vector_store.py # Cria a base vetorial (Chroma)
├── chunk_texts.py # Segmenta textos em chunks
├── create_embeddings.py # Gera embeddings em lote
├── extract_anvisa.py # Extrai e limpa documentos ANVISA
├── extract_ministerio_saude.py # Extrai portarias do Ministério da Saúde
├── extract_ministerio_tuss.py # Processa tabela TUSS
├── query_vector_store.py # Consulta a base vetorial
└── text_utils.py # Funções utilitárias (log, tokenização, etc.)
```

---

## 🚀 Execução

### 1️⃣ Criar ambiente virtual

```bash
python -m venv .venv
source .venv/bin/activate
.venv\Scripts\activate
```

### 2️⃣ Instalar dependências

```bash
pip install -r requirements.txt
```

### 3️⃣ Executar o pipeline completo

```bash
# Extração e limpeza
python src/extract_anvisa.py
python src/extract_ministerio_saude.py
python src/extract_ministerio_tuss.py

# Chunking e embeddings
python src/chunk_texts.py
python src/create_embeddings.py

# Construção da base vetorial
python src/build_vector_store.py

# Testar busca semântica
python src/query_vector_store.py

🔍 Consulta: Qual a regulamentação para produtos saneantes com ação antimicrobiana?

📦 Base carregada: 18.540 embeddings disponíveis.

Resultado 1 (score=0.0863):
   🏷️ Categoria: regulacao
   🗂️ Fonte: anvisa
   🌐 Source: ../data/raw/anvisa/Nota Técnica 20_2021 tecidos com ação antimicrobiana.pdf

   📄 Trecho: 14, DE 28 DE FEVEREIRO DE 2007. Aprova o RegulamentoTécnico para Produtos Saneantes com Ação Anmicrobiana harmonizado no âmbito do Mercosulatravés da Resolução GMC no 50/06, que consta em anexo à presente Resolução. Acessado em03/07/2020, disponível em: hps://www.cevs.rs.gov.br/upload/arquivos/201611/08140937-rdc-14-2007.pdf5. BRASIL. ANVISA/MS. INSTRUÇÃO NORMATIVA No 4, DE 2 DE JULHO DE 2013. Dispõe sobre os critériosde aceitação de relatórios de ensaios exigidos para análise dos pedidos de noficação e registro deprodutos saneantes e dá outras providências. Acessado em 03/07/2020, disponívelem: hps://bvsms.saude.gov.br/bvs/saudelegis/anvisa/2013/int0004_02_07_2013.html6. BRASIL. ANVISA/MS. INSTRUÇÃO NORMATIVA No 12, DE 11 DE OUTUBRO DE 2016. Altera a InstruçãoNormava - IN
```

## 🧾 Fontes Oficiais

- ANVISA — Portal de Legislação Sanitária
- Ministério da Saúde — Base de Portarias e Normas
- TUSS (ANS) — Terminologia Unificada da Saúde Suplementar