
from utils.pdfLoader.PyMuPDFLoader import PDF_PyMuPDFLoader
from utils.pyPDF import get_document_chunks
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

    embeddings = OpenAIEmbeddings(openai_api_key=st.secrets["api_keys"]["OPEN_API_KEY"])
    vector_store = FAISS.load_local("faiss_index", embeddings)

    query = "横断勾配は？"
    embedding_vector = embeddings.embed_query(query)
    docs_and_scores = vector_store.similarity_search_by_vector(embedding_vector)

    for c in docs_and_scores:
        # print(c.metadata)
        print(c.metadata['source'])
        print(c.metadata['page'])

    
    # print(docs_and_scores)
    
    # load_qa_chainを準備
    chain = load_qa_chain(ChatOpenAI(
        openai_api_key=st.secrets["api_keys"]["OPEN_API_KEY"],
        temperature=0), chain_type="stuff")


    print(chain({"input_documents": docs_and_scores, "question": query}, return_only_outputs=True))
    
    # print(chain({"input_documents": docs_and_scores, "question": query}))

if __name__ == "__main__":
    main()
