from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings

import streamlit as st


def get_vectorstore(text_chunks):

    # create embeddings before loading into a vector store/knowledge base
    embeddings = OpenAIEmbeddings(openai_api_key=st.secrets["api_keys"]["OPEN_API_KEY"])

    # we'll use FAISS as our vector store.
    vector_store = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vector_store