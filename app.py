import os
import tempfile
import streamlit as st
from dotenv import load_dotenv

from indexador import indexar_pdf
from perguntador import responder_pergunta

load_dotenv()

st.set_page_config(page_title="Vero — Pergunte ao Documento", page_icon="🔎")
st.title("🔎 Vero — seu assistente de documentos")
st.caption("Suba um PDF e converse com o conteúdo dele. Toda resposta vem direto do documento, nunca inventada.")

# Guarda se já indexamos um documento nessa sessão
if "documento_indexado" not in st.session_state:
    st.session_state.documento_indexado = False
if "mensagens" not in st.session_state:
    st.session_state.mensagens = []

# --- Upload do PDF ---
with st.sidebar:
    st.markdown("### 🔎 Vero")
    st.caption("Respostas baseadas 100% no que está no seu documento — nunca inventadas.")
    st.divider()
    
    
    st.header("📁 Seu documento")
    arquivo = st.file_uploader("Envie um PDF", type="pdf")

    if arquivo is not None:
        if st.button("Indexar documento"):
            with st.spinner("Lendo e indexando o documento..."):
                # Salva o upload temporariamente em disco pra poder ler com pypdf
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    tmp.write(arquivo.read())
                    caminho_temp = tmp.name

                total_chunks = indexar_pdf(caminho_temp)
                os.unlink(caminho_temp)  # remove o arquivo temporário

                st.session_state.documento_indexado = True
                st.session_state.mensagens = []  # limpa histórico do documento anterior

            st.success(f"Documento indexado! ({total_chunks} trechos)")

# --- Chat ---
if not st.session_state.documento_indexado:
    st.info("👋 Sou o Vero! Envie um PDF na barra lateral e clique em 'Indexar documento' para começarmos a conversar sobre ele.")
else:
    for msg in st.session_state.mensagens:
        avatar = "🧑‍💻" if msg["role"] == "user" else "🔎"
        with st.chat_message(msg["role"], avatar=avatar):
            st.write(msg["conteudo"])

    pergunta = st.chat_input("Pergunte algo sobre o documento...")

    if pergunta:
        st.session_state.mensagens.append({"role": "user", "conteudo": pergunta})
        with st.chat_message("user"):
            st.write(pergunta)

        with st.chat_message("assistant", avatar="🔎"):
            with st.spinner("Buscando no documento..."):
                resposta = responder_pergunta(pergunta)
                st.write(resposta)

        st.session_state.mensagens.append({"role": "assistant", "conteudo": resposta})