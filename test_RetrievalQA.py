
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
import streamlit as st
import os
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA

# proxy設定
os.environ['http_proxy'] = st.secrets["proxy"]["URL"]
os.environ['https_proxy'] = st.secrets["proxy"]["URL"]


def main():

    embeddings = OpenAIEmbeddings(openai_api_key=st.secrets["api_keys"]["OPEN_API_KEY"])
    vector_store = FAISS.load_local("faiss_index", embeddings)

    qa = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(openai_api_key=st.secrets["api_keys"]["OPEN_API_KEY"]), chain_type="stuff", retriever=vector_store.as_retriever(), return_source_documents=True)
    query = "横断勾配は何％？"

    # result = qa({"query": query})
    
    # test = 

    # print(vector_store.as_retriever().get_relevant_documents(query=query))
    print(qa({"query": query}))
    # print(qa.run(query))



if __name__ == "__main__":
    main()
