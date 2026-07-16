from pathlib import Path
import os
import streamlit as st

from dotenv import load_dotenv

from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")

if not GOOGLE_API_KEY:
    GOOGLE_API_KEY = st.secrets.get("GEMINI_API_KEY")

_vectorstore = None
_llm = None

def inicializar():
    global _vectorstore, _llm

    if _vectorstore is None:
        _vectorstore = cargar_vectorstore()

    if _llm is None:
        _llm = crear_modelo_gemini()

   

def cargar_documentos():
    """
    Lee todos los PDF ubicados en la carpeta documentos/
    y devuelve una lista de documentos de LangChain.
    """

    documentos = []

    for archivo in Path("documentos").glob("*.pdf"):

        loader = PyMuPDFLoader(str(archivo))

        documentos.extend(loader.load())

    print(f"📄 PDFs cargados: {len(documentos)}")

    return documentos

def dividir_documentos(documentos):
    """
    Divide los documentos en fragmentos más pequeños
    para poder generar embeddings.
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    documentos_divididos = splitter.split_documents(documentos)


    return documentos_divididos

def crear_vectorstore(documentos_divididos):
    """
    Genera embeddings de los fragmentos de documentos
    y crea un índice vectorial FAISS.
    """

    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=GOOGLE_API_KEY
    )

    vectorstore = FAISS.from_documents(
        documents=documentos_divididos,
        embedding=embeddings
    )

    vectorstore.save_local("vectorstore")

  

    return vectorstore

def cargar_vectorstore():
    """
    Carga el vectorstore FAISS guardado en disco.
    """

    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=GOOGLE_API_KEY
    )

    vectorstore = FAISS.load_local(
        "vectorstore",
        embeddings,
        allow_dangerous_deserialization=True
    )


    return vectorstore

def probar_busqueda(vectorstore):
    """
    Realiza una búsqueda de prueba dentro de los documentos.
    """

    pregunta = "¿Cuáles son los derechos del paciente?"

    resultados = vectorstore.similarity_search(
        pregunta,
        k=3
    )

    print("\n🔎 Resultados encontrados:")

    for i, documento in enumerate(resultados):
        print("\n--- Resultado", i + 1, "---")
        print(documento.page_content[:500])
        print("Metadata:", documento.metadata)
    
    contexto = "\n\n".join(
        documento.page_content
        for documento in documentos
    )

   

def crear_modelo_gemini():
    """
    Crea el modelo Gemini encargado de generar respuestas.
    """

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=GOOGLE_API_KEY,
        temperature=0
    )

    return llm

def responder_pregunta( pregunta, vectorstore=None):
    """
    Busca información relevante y genera una respuesta con Gemini.
    """
    if vectorstore is None:
        vectorstore = _vectorstore

    if vectorstore is None:
        raise RuntimeError(
            "El vectorstore no está inicializado. Llama a inicializar() o pásalo como parámetro."
        )
    documentos = vectorstore.similarity_search(
        pregunta,
        k=4
    )

    contexto = "\n\n".join(
        documento.page_content
        for documento in documentos
    )

    prompt = f"""
    Responde la pregunta utilizando únicamente el contexto entregado.

    Si la información no está en el contexto,
    indica que no existe información disponible.

    Contexto:
    {contexto}

    Pregunta:
    {pregunta}
    """

    llm = crear_modelo_gemini()

    respuesta = llm.invoke(prompt)

    return respuesta.content


