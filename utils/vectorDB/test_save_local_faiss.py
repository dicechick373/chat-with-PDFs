
# from app.pdfLoader.PyMuPDFLoader import PDF_PyMuPDFLoader
# from app.pyPDF import get_document_chunks
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
import streamlit as st
import os
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI

# proxy設定
os.environ['http_proxy'] = st.secrets["proxy"]["URL"]
os.environ['https_proxy'] = st.secrets["proxy"]["URL"]


def main():

    # PDFを指定
    # pdf_path = "data\pdf\土木技術管理規程集_道路Ⅱ編_テスト1.pdf"

    # # Documentに変換
    # data = PDF_PyMuPDFLoader(pdf_path)

    # chunks = get_document_chunks(data)

    # # Get embedding model
    # embeddings = OpenAIEmbeddings(openai_api_key=st.secrets["api_keys"]["OPEN_API_KEY"])
    # #  vector databaseの作成
    # db = FAISS.from_documents(chunks, embeddings)

    # # ローカルに保存
    # db.save_local("faiss_index/test")


    embeddings = OpenAIEmbeddings(openai_api_key=st.secrets["api_keys"]["OPEN_API_KEY"])
    vector_store = FAISS.load_local("faiss_index", embeddings)

    query = "横断勾配は？"
    embedding_vector = embeddings.embed_query(query)
    docs_and_scores = vector_store.similarity_search_by_vector(embedding_vector)
    
    
    # load_qa_chainを準備
    chain = load_qa_chain(ChatOpenAI(
        openai_api_key=st.secrets["api_keys"]["OPEN_API_KEY"],
        temperature=0), chain_type="stuff")


    # print(chain({"input_documents": docs_and_scores, "question": query}, return_only_outputs=True))
    
    print(chain({"input_documents": docs_and_scores, "question": query}))

if __name__ == "__main__":
    main()
