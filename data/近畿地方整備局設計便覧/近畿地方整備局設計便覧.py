
from langchain.llms import OpenAIChat
import streamlit as st
import os
import json
import glob
from langchain.document_loaders import PyMuPDFLoader


# utilsのimport
import sys
sys.path.append('D:/GoogleDrive/マイドライブ/github_repositories/chat-with-PDFs')
from utils import PDFMiner
# sys.path.append('PATH_TO_TENSORFLOW_OBJECT_DETECTION_FOLDER')

# OpenAIを利用するためにプロキシ設定が必要
os.environ['http_proxy'] = st.secrets["proxy"]["URL"]
os.environ['https_proxy'] = st.secrets["proxy"]["URL"]

llm = OpenAIChat(openai_api_key=st.secrets["api_keys"]["OPEN_API_KEY"],temperature=0.0)

def format_text(page_content):
    prompt = f'''
        以下に示すデータは、PDF形式の文書をPDFyMuPDFLoaderによりテキスト化したものである。
        このデータから、下記のルールに従ってJSONデータに変換せよ。
        JSONデータが途中で切れている場合は、その部分を削除して、正規のJSONデータに変換せよ。

        ルール:
        - JSONのキーは'text'とする。
        - 全角英数字は、半角英数字に変換する。
        - 文字間の空白は、全て削除する。
        - 二重引用符（"）、バックスラッシュ（\）、改行文字（\n）、タブ文字（\t）などの特殊文字が含まれる場合は、エスケープ文字を付与する。
        
        # データ
        {page_content}]
        '''
    
    return llm(prompt)

# def format_metadata(page_content):
#     prompt = f'''
#         以下に示すデータは、PDF形式の文書をPDFyMuPDFLoaderによりテキスト化したものである。
#         このデータから、下記のルールに従ってページ番号をJSONデータに変換せよ。

#         ルール:
#         - 最下部のテキストをページ番号とする。改行コードは削除する。
#         - JSONのキーは'page_number'とする。
        
#         # データ
#         {page_content}]
#         '''
#     return llm(prompt)

def format_table(page_content):
    prompt = f'''
        以下に示すデータは、PDF形式の文書をPDFyMuPDFLoaderによりテキスト化したものである。
        このデータから、表形式として認識できる情報を全て、下記のルールに従ってJSONデータに変換せよ。
        表形式の情報が複数ある場合は、全ての情報をJSONデータに変換せよ。

        ルール:
        - JSONのキーは'table'とする。
        - '表'を含むテキストの下部に、表形式の情報があることが多い。   
        - 表のタイトルは、表の上にある文章として認識する。JSONのキーは'title'とする。
        - 表の内容は、表形式のjsonに変換する。JSONのキーは'data'とする。
        - 二重引用符（"）、バックスラッシュ（\）、改行文字（\n）、タブ文字（\t）などの特殊文字が含まれる場合は、エスケープ文字を付与する。
        
        # データ
        {page_content}]
        '''
    
    return llm(prompt)


def format_dict(data):
    content = data.page_content.replace("（", "(") \
    .replace("）", ")") \
    .replace("－", "-") \
    .replace("：", ":") \
    .replace("［", "[") \
    .replace("］", "]")

    print(content)
    print(format_text(content))
    text = json.loads(format_text(content))['text']
    print(text)
    table = json.loads(format_table(content))['table']
    print(table)

    return {
        "text": text,
        "table": table,
    }



def main():
    pdf_path = 'data\近畿地方整備局設計便覧\PDF_READ\土木工事共通編.pdf'

    # pdfminerのレイアウト分析
    pdfminer = PDFMiner.PDFTextAnalyzer(pdf_path)
    top_of_y_coord = 48 # ページ番号を取得するためのしきい値（y座標）を設定
    pages = pdfminer.get_page_number(top_of_y_coord)
    # print(len(pages)) # 総ページ数の確認　

    from langchain.document_loaders import PDFMinerLoader
    loader = PDFMinerLoader(pdf_path)
    data= loader.load_and_split()

    # test = data[16]
    print(format_dict(data[16]))
   
    # for i, d in enumerate(data):

    #     # ページ番号を取得
    #     page = pages[i]

    #     # 保存先の設定
    #     dir_path= f'data/近畿地方整備局設計便覧/JSON/土木工事共通編'
    #     os.makedirs(dir_path, exist_ok=True)

    #     # すでに存在する場合はスキップ
    #     json_path = f'{dir_path}/土木工事共通編_{page}.json'
    #     if os.path.isfile(json_path):
    #         print(f'{page}はすでに存在します。')
    #         continue
        
    #     # データの整形
    #     dict_data = format_dict(d)
    #     dict_data["page_number"] = page

    #     # JSONに保存
    #     with open(f'{dir_path}/土木工事共通編_{page}.json', 'w',  encoding='utf-8') as f:
    #         json.dump(dict_data, f, indent=2, ensure_ascii=False)
    #         print(f'{page}を保存しました。')

    
if __name__ == '__main__':
    main()