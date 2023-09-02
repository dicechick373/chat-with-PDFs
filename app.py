# import modules
import streamlit as st
from app import chain

# Set up proxy configuration
from app import proxy
proxy.configure_proxy()

def main():
    st.set_page_config(page_title="Chat with multiple PDFs",
                       page_icon="🤓")
    
 
    st.header("Chat with multiple PDFs 📚")

    # 質問の入力欄を作成
    question = st.text_input("質問を入力してください")
    
    if st.button("送信"):
        response = chain.answer_with_source(question)
        st.write("回答:\n", response['answer'])
        st.write("出典:\n", response['source'])



    # Sidebar
    with st.sidebar:
        st.subheader("土木技術管理規定集")
        agree = st.checkbox('道路Ⅰ編')
        # pdf_docs = st.file_uploader(
        #     "Upload your PDFs here and click `Process`", accept_multiple_files=True)
        
        # with st.expander("土木技術管理規定集"):
        #     agree = st.checkbox('I agree')
        
       

        # if st.button("Process"):
        #     with st.spinner("Processing files ..."):
        #         # get raw pdf text
        #         # raw_text = pyPDF.get_pdf_text(pdf_docs)

        #         # segment raw pdf text into chunks
        #         # text_chunks = pyPDF.get_text_chunks(raw_text)

        #         # load text chunks into a vector store
        #         # vectorstore= vector_FAISS.get_vectorstore(text_chunks)

        #         # vectorstore= vector_FAISS.get_vectorstore_local()

        #         # create conversation chain
        #         st.session_state.conversation = chain.get_conversation_chain(vectorstore)

if __name__ == "__main__":
    main()
