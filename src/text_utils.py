import json
import time
from pathlib import Path
import tiktoken


def log_info(message: str):
    """
    Exibe mensagens padronizadas com timestamp.

    Args:
        message (str): texto a ser exibido no log.
    """
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")


def load_jsonl(path: str):
    """
    Lê um arquivo .jsonl e retorna uma lista de dicionários.

    Args:
        path (str): caminho do arquivo .jsonl.

    Returns:
        list[dict]: lista de registros carregados.
    """
    path_obj = Path(path)
    if not path_obj.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {path}")

    with open(path, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def count_tokens(text: str, model_name: str = "gpt-3.5-turbo"):
    """
    Conta o número aproximado de tokens em um texto.

    Args:
        text (str): texto de entrada.
        model_name (str): nome do modelo compatível com tiktoken.

    Returns:
        int: número de tokens estimado.
    """
    try:
        enc = tiktoken.encoding_for_model(model_name)
    except KeyError:
        enc = tiktoken.get_encoding("cl100k_base")  # fallback genérico
    return len(enc.encode(text))


def chunk_text(text: str, max_tokens: int = 500, model_name: str = "gpt-3.5-turbo"):
    """
    Divide um texto em pedaços (chunks) de tamanho aproximado definido por tokens.

    Args:
        text (str): texto de entrada.
        max_tokens (int): limite máximo de tokens por chunk.
        model_name (str): modelo para cálculo dos tokens.

    Returns:
        list[str]: lista de chunks de texto.
    """
    try:
        enc = tiktoken.encoding_for_model(model_name)
    except KeyError:
        enc = tiktoken.get_encoding("cl100k_base")

    tokens = enc.encode(text)
    chunks = []
    for i in range(0, len(tokens), max_tokens):
        chunk = enc.decode(tokens[i:i + max_tokens])
        chunks.append(chunk.strip())
    return chunks