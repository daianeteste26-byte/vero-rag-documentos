import os
from dotenv import load_dotenv
from google import genai
import chromadb

from extrator import extrair_texto_pdf

load_dotenv()
client_gemini = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Cliente do ChromaDB (banco vetorial local, salva em disco)
client_chroma = chromadb.PersistentClient(path="./banco_vetorial")
colecao = client_chroma.get_or_create_collection(name="documentos")


def dividir_em_chunks(texto: str, tamanho: int = 500, sobreposicao: int = 50) -> list[str]:
    """
    Divide um texto longo em pedaços menores (chunks), com uma pequena
    sobreposição entre eles para não perder contexto nas bordas.
    """
    chunks = []
    inicio = 0

    while inicio < len(texto):
        fim = inicio + tamanho
        chunks.append(texto[inicio:fim])
        inicio += tamanho - sobreposicao

    return chunks


def gerar_embedding(texto: str) -> list[float]:
    """
    Transforma um texto em uma lista de números (embedding) usando o Gemini.
    """
    resultado = client_gemini.models.embed_content(
        model="gemini-embedding-001",
        contents=texto
    )
    return resultado.embeddings[0].values


def indexar_pdf(caminho_pdf: str):
    """
    Pipeline completo: extrai texto do PDF, divide em chunks,
    gera embeddings e salva no ChromaDB.
    """
    # Limpa indexações anteriores antes de indexar um novo documento
    global colecao
    client_chroma.delete_collection(name="documentos")
    colecao = client_chroma.get_or_create_collection(name="documentos")

    texto = extrair_texto_pdf(caminho_pdf)
    chunks = dividir_em_chunks(texto)

    for i, chunk in enumerate(chunks):
        embedding = gerar_embedding(chunk)
        colecao.add(
            ids=[f"chunk_{i}"],
            embeddings=[embedding],
            documents=[chunk]
        )

    return len(chunks)