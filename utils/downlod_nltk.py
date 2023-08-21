import os
import streamlit as st

# proxy設定
os.environ['http_proxy'] = st.secrets["proxy"]["URL"]
os.environ['https_proxy'] = st.secrets["proxy"]["URL"]


import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')