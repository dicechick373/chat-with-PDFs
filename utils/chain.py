
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain import PromptTemplate
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from langchain.chains.conversational_retrieval.prompts import CONDENSE_QUESTION_PROMPT
from langchain.chains import LLMChain

def get_conversation_chain(vectorstore):
    
    llm = ChatOpenAI(openai_api_key=st.secrets["api_keys"]["OPEN_API_KEY"],
                     temperature=0.25,model_name='gpt-3.5-turbo-16k')
 
    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )

    # print(conversation_chain)
    
    return conversation_chain

class AnswerConversationBufferMemory(ConversationBufferMemory):
    def save_context(self, inputs, outputs) :
        return super(AnswerConversationBufferMemory, self).save_context(inputs,{'response': outputs['answer']})


# def get_conversation_with_sources_chain(vectorstore):
    
#     llm = ChatOpenAI(openai_api_key=st.secrets["api_keys"]["OPEN_API_KEY"],
#                      temperature=0.25,model_name='gpt-3.5-turbo-16k')
    
#     question_generator = LLMChain(llm=llm, prompt=CONDENSE_QUESTION_PROMPT)
#     doc_chain = load_qa_with_sources_chain(llm, chain_type="map_reduce")
    
#     memory = AnswerConversationBufferMemory(
#         memory_key="chat_history", return_messages=True)
        
#     conversation_chain = ConversationalRetrievalChain(
#         retriever=vectorstore.as_retriever(),
#         question_generator=question_generator,
#         memory=memory, 
#         combine_docs_chain=doc_chain,
#     )
#     return conversation_chain

