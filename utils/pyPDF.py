# import streamlit as st
from PyPDF2 import PdfReader

from langchain.text_splitter import CharacterTextSplitter

def get_pdf_text(pdf_docs):
    """
    Converts the text content of PDF documents into a single text string.

    Args:
        pdf_docs (list): List of paths to PDF documents.

    Returns:
        str: Concatenated text content extracted from all PDF pages.
    """
    text = ""

    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    
    return text


def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size = 800,
        chunk_overlap=200,
        length_function = len
    )
    chunks = text_splitter.split_text(text)
    return chunks
