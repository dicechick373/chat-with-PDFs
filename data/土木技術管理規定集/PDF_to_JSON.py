# utilsのimport
import sys
sys.path.append('D:/GoogleDrive/マイドライブ/github_repositories/chat-with-PDFs')
from utils import PDFMiner
import os
import streamlit as st
from paddleocr import PaddleOCR, draw_ocr

# OpenAIを利用するためにプロキシ設定が必要
os.environ['http_proxy'] = st.secrets["proxy"]["URL"]
os.environ['https_proxy'] = st.secrets["proxy"]["URL"]


def main():

    ocr = PaddleOCR(lang="japan")
    img_path = 'data\土木技術管理規定集\テスト.pdf'
    result = ocr.ocr(img_path)
    for idx in range(len(result)):
        res = result[idx]
        for line in res:
            print(line)

   



    
if __name__ == '__main__':
    main()
