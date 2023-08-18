import os
import streamlit as st

from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

# import modules
from utils import pyPDF
from utils import vector_FAISS



# proxy設定
os.environ['http_proxy'] = st.secrets["proxy"]["URL"]
os.environ['https_proxy'] = st.secrets["proxy"]["URL"]


def get_conversation_chain(vectorstore):
    
    llm = ChatOpenAI(openai_api_key=st.secrets["api_keys"]["OPEN_API_KEY"],
                     temperature=0.25)

    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain

def handle_user_input(user_question):
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        if i%2 == 0:
            user = st.chat_message(name="User", avatar="💃")
            user.write(message.content)
        else:
            assistant = st.chat_message(name="J.A.A.F.A.R.", avatar="🤖")
            assistant.write(message.content)

def main():
    st.set_page_config(page_title="Chat with multiple PDFs",
                       page_icon="🤓")
    
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None
    
    st.header("Chat with multiple PDFs 📚")
    user_question = st.text_input("Ask a question about your documents:")
    if user_question:
        handle_user_input(user_question)

    """
    Sidebar
    """
    with st.sidebar:
        st.subheader("Your documents")
        pdf_docs = st.file_uploader(
            "Upload your PDFs here and click `Process`", accept_multiple_files=True)
        if st.button("Process"):
            with st.spinner("Processing files ..."):
                # get raw pdf text
                raw_text = pyPDF.get_pdf_text(pdf_docs)

                # segment raw pdf text into chunks
                text_chunks = pyPDF.get_text_chunks(raw_text)

                # load text chunks into a vector store
                vectorstore= vector_FAISS.get_vectorstore(text_chunks)

                # create conversation chain
                st.session_state.conversation = get_conversation_chain(vectorstore)

if __name__ == "__main__":
    main()