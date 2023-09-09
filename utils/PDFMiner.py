
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LAParams, LTTextContainer
from pdfminer.converter import PDFPageAggregator

class PDFTextAnalyzer:
    """
    PDF文書内のテキストを分析するクラス。PDFMinerを使用。

    Args:
        pdf_path (str): 分析対象のPDF文書のパス。

    Attributes:
        pdf_path (str): PDF文書のパス。
    
    Methods:
        get_page_number(self, top_of_y_coord):
            指定したY座標を基準にPDF文書からページ番号を抽出。
    """

    def __init__(self, pdf_path):
        """
        PDFTextAnalyzerインスタンスの初期化。

        Args:
            pdf_path (str): 分析対象のPDF文書のパス。
        """
        self.pdf_path = pdf_path

    def get_page_number(self, top_of_y_coord):
        """
        指定したY座標を基準にPDF文書からページ番号を抽出。

        Args:
            top_of_y_coord (int): ページ番号抽出のY座標の閾値。

        Returns:
            str: 抽出されたページ番号（見つからない場合は空文字列）。
        """
        return _page_numbers(self.pdf_path, top_of_y_coord)
                             
    def get_layouts(self):
        return _layouts(self.pdf_path)
        
        
def _page_numbers(pdf_path,top_of_y_coord):
    manager = PDFResourceManager()

    result = []
    with open(pdf_path, 'rb') as input:
        with PDFPageAggregator(manager, laparams=LAParams()) as device:
            # PDFPageInterpreterオブジェクトの取得
            iprtr = PDFPageInterpreter(manager, device)
            # ページごとで処理を実行
            for page in PDFPage.get_pages(input):
                iprtr.process_page(page)
                # ページ内の各テキストのレイアウト
                layouts = device.get_result()

                page_number = _analysis_page_number(layouts,top_of_y_coord)
                result.append(page_number)
    return result

def _analysis_page_number(layouts,top_of_y_coord):
    for layout in layouts:
        if isinstance(layout, LTTextContainer):
            if layout.y1 < top_of_y_coord:
                return layout.get_text().strip()
                        
    return ''

def _layouts(pdf_path):
    manager = PDFResourceManager()

    result = []
    with open(pdf_path, 'rb') as input:
        with PDFPageAggregator(manager, laparams=LAParams()) as device:
            # PDFPageInterpreterオブジェクトの取得
            iprtr = PDFPageInterpreter(manager, device)
            # ページごとで処理を実行
            for page in PDFPage.get_pages(input):
                iprtr.process_page(page)
                # ページ内の各テキストのレイアウト
                layouts = device.get_result()
                result.append(_analysis_layout(layouts))
    return result


def _analysis_layout(layouts):
    result = []
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
            # print(paragraph)

            result.append(paragraph)

    return result