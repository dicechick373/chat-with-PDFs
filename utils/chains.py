
import os
import streamlit as st
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI


# Set up proxy configuration
os.environ['http_proxy'] = st.secrets["proxy"]["URL"]
os.environ['https_proxy'] = st.secrets["proxy"]["URL"]

# Initialize embeddings and vector store outside of the function to avoid repetitive API calls
embeddings = OpenAIEmbeddings(openai_api_key=st.secrets["api_keys"]["OPEN_API_KEY"])
vector_store = FAISS.load_local("faiss_index", embeddings)

def answer_with_source(query):

    embedding_vector = embeddings.embed_query(query)
    docs_and_scores = vector_store.similarity_search_by_vector(embedding_vector)

    # load_qa_chainを準備
    chain = load_qa_chain(ChatOpenAI(
        openai_api_key=st.secrets["api_keys"]["OPEN_API_KEY"],
        temperature=0), chain_type="stuff")
    
    
    responses = chain.run(input_documents=docs_and_scores, question=query)

    source_list = [f"{doc.metadata['source']}:P{doc.metadata['page']}" for doc in docs_and_scores]
    source_str = ', '.join(source_list)


    return {
        'answer':responses,
        'source':source_str
    }
    


if __name__ == "__main__":
    answer_with_source()
