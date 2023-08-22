
from utils.pdfLoader.PyMuPDFLoader import PDF_PyMuPDFLoader
from utils.pyPDF import get_document_chunks
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
import streamlit as st
import os

# proxy設定
os.environ['http_proxy'] = st.secrets["proxy"]["URL"]
os.environ['https_proxy'] = st.secrets["proxy"]["URL"]


def main():

    # PDFを指定
    pdf_path = "data/pdf/土木技術管理規程集_道路Ⅱ編.pdf"

    # Documentに変換
    data = PDF_PyMuPDFLoader(pdf_path)

    chunks = get_document_chunks(data)

    # Get embedding model
    embeddings = OpenAIEmbeddings(openai_api_key=st.secrets["api_keys"]["OPEN_API_KEY"])
    #  vector databaseの作成
    db = FAISS.from_documents(chunks, embeddings)

    # ローカルに保存
    db.save_local("faiss_index")

    

    # print(chunks)

 

if __name__ == "__main__":
    main()
