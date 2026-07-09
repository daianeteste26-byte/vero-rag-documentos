from pypdf import PdfReader

def extrair_texto_pdf(caminho_arquivo: str) -> str:
    """
    Lê um arquivo PDF e retorna todo o texto extraído.
    """
    leitor = PdfReader(caminho_arquivo)
    texto_completo = ""

    for pagina in leitor.pages:
        texto_completo += pagina.extract_text() + "\n"

    return texto_completo


if __name__ == "__main__":
    texto = extrair_texto_pdf("teste.pdf")
    print(f"Total de caracteres extraídos: {len(texto)}\n")
    print("Primeiros 500 caracteres:\n")
    print(texto[:500])