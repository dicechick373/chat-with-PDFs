
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LAParams, LTTextContainer
from pdfminer.converter import PDFPageAggregator


# PDFのレイアウト分析
def pdfminer_layout_analysis(layouts):
    # 結果を格納する辞書
    result = {
        'contents':[],
        'page':'',
    }
    
    for layout in layouts:
        # 罫線などのオブジェクトが含まれているとエラーになるのを防ぐため
        if isinstance(layout, LTTextContainer):
            # 座標は各ページの左下を原点としている
            paragraph = {
                'text':layout.get_text().strip(),
                'x0':round(layout.x0,2),# x0: テキストの左端のx座標
                'x1':round(layout.x1,2),# x1: テキストの右端のx座標
                'y0':round(layout.y0,2),# y0: テキストの下端のy座標
                'y1':round(layout.y1,2),# y1: テキストの上端のy座標
                'width':round(layout.width,2),# width: テキストの幅(x1 - x0)
                'height':round(layout.height,2),# height: テキストの高さ(y1 - y0)
            }
                        
            # ページ番号を格納する（y座標<48で判別できる）
            if layout.y1 < 48:
                # print('page number'+layout.get_text().strip())
                result['page'] = layout.get_text().strip()
                        
            # 出典は除外する（x座標>467で判別できる）
            if layout.x0 > 467:
                # print('source'+layout.get_text().strip())
                continue
            
            # 結果を格納
            result['contents'].append(paragraph)
        
    return result


def pdfminer(path):
    manager = PDFResourceManager()

    result = []

    with open(path, 'rb') as input:
        with PDFPageAggregator(manager, laparams=LAParams()) as device:
            # PDFPageInterpreterオブジェクトの取得
            iprtr = PDFPageInterpreter(manager, device)
            # ページごとで処理を実行
            for page in PDFPage.get_pages(input):
                iprtr.process_page(page)
                # ページ内の各テキストのレイアウト
                layouts = device.get_result()

                # レイアウト分析結果
                contents = pdfminer_layout_analysis(layouts)
                result.append(contents)
    
    return result


def main():
    pdf_path = 'data\近畿地方整備局設計便覧\テスト.pdf'
    result = pdfminer(pdf_path)

    from langchain.document_loaders import PDFMinerLoader
    loader = PDFMinerLoader(pdf_path)
    data= loader.load_and_split()
    
    print(data[0])



if __name__ == '__main__':
    main()