pipeline:
	python src/extract_anvisa.py
	python src/extract_ministerio_saude.py
	python src/extract_ministerio_tuss.py
	python src/chunk_texts.py
	python src/create_embeddings.py
	python src/build_vector_store.py
	python src/query_vector_store.py
	python src/query_llm.py
