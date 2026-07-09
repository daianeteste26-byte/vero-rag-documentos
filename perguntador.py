import os
from dotenv import load_dotenv
from google import genai
import chromadb

load_dotenv()
client_gemini = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

client_chroma = chromadb.PersistentClient(path="./banco_vetorial")
colecao = client_chroma.get_or_create_collection(name="documentos")


def buscar_chunks_relevantes(pergunta: str, quantidade: int = 3) -> list[str]:
    """
    Transforma a pergunta em embedding e busca os chunks mais parecidos
    (por significado) dentro do banco vetorial.
    """
    # Busca a coleção "fresca" a cada chamada, evitando referência desatualizada
    colecao_atual = client_chroma.get_or_create_collection(name="documentos")

    resultado_embedding = client_gemini.models.embed_content(
        model="gemini-embedding-001",
        contents=pergunta
    )
    embedding_pergunta = resultado_embedding.embeddings[0].values

    resultados = colecao_atual.query(
        query_embeddings=[embedding_pergunta],
        n_results=quantidade
    )

    return resultados["documents"][0]


def responder_pergunta(pergunta: str) -> str:
    """
    Pipeline completo de RAG: busca os trechos relevantes do documento
    e pede pro Gemini responder usando só esse contexto.
    """
    chunks_relevantes = buscar_chunks_relevantes(pergunta)
    contexto = "\n\n---\n\n".join(chunks_relevantes)

    prompt = f"""Responda a pergunta do usuário usando APENAS as informações do contexto abaixo.
Se a resposta não estiver no contexto, diga claramente que não encontrou essa informação no documento.

Contexto:
{contexto}

Pergunta: {pergunta}

Resposta:"""

    resposta = client_gemini.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return resposta.text


if __name__ == "__main__":
    print("Pergunte algo sobre o documento (ou 'sair' para encerrar).\n")

    while True:
        pergunta = input("Você: ")
        if pergunta.lower() == "sair":
            break

        resposta = responder_pergunta(pergunta)
        print(f"\nResposta: {resposta}\n")