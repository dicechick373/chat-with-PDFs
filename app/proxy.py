import os
import streamlit as st

# Set up proxy configuration
def configure_proxy():
    os.environ['http_proxy'] = st.secrets["proxy"]["URL"]
    os.environ['https_proxy'] = st.secrets["proxy"]["URL"]