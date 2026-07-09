# 🔎 Vero — Pergunte ao Documento

Um assistente que responde perguntas com base no conteúdo real de um PDF que você envia — nunca inventa informação, só usa o que está escrito no documento.

![Status](https://img.shields.io/badge/status-funcionando-brightgreen)

## O que ele faz

1. Você envia um PDF
2. O Vero lê, organiza e "entende" o conteúdo
3. Você pergunta qualquer coisa sobre esse documento
4. Ele busca as partes relevantes e responde com base nelas

## Como funciona (RAG — Retrieval-Augmented Generation)

A ideia central: uma IA sozinha não sabe nada sobre o seu documento específico. Então, antes de perguntar pra IA, o sistema primeiro **busca os trechos certos** dentro do PDF, e só depois pede pra IA responder usando aquele trecho como base.

O truque de transformar texto em números (**embedding**) é o que permite buscar por **significado**, não só por palavra exata. Por isso o sistema encontra a resposta certa mesmo que você não use as mesmas palavras do documento.

## Tecnologias usadas

- **Python** — lógica do projeto
- **pypdf** — extrai o texto de dentro do PDF
- **Gemini API** — gera os embeddings e responde as perguntas
- **ChromaDB** — banco de dados vetorial, guarda os pedaços do documento de forma buscável
- **Streamlit** — interface web com upload de arquivo e chat

## Rodando localmente

```bash
git clone https://github.com/daianeteste26-byte/vero-rag-documentos.git
cd vero-rag-documentos
python -m venv venv
venv\Scripts\activate       # Windows
python -m pip install -r requirements.txt
```

Crie um arquivo `.env` na raiz com:
GEMINI_API_KEY=sua_chave_aqui

Rode com:
```bash
streamlit run app.py
```

## Decisões técnicas

- **Reindexação limpa a cada novo PDF**: sempre que um novo documento é enviado, o banco vetorial antigo é apagado antes de indexar o novo — evita que perguntas misturem conteúdo de arquivos diferentes.
- **Resposta restrita ao contexto**: o prompt instrui explicitamente a IA a dizer quando a resposta não está no documento, em vez de inventar uma resposta genérica.

## Sobre mim

Sou a Daiane, em transição de carreira para tecnologia e IA. Esse projeto foi minha forma de aprender RAG na prática — um dos conceitos mais usados hoje em assistentes que respondem com base em documentos reais, como contratos, manuais e apostilas.