"""Convert webpage or html files (1 or multiple) to pdf file.
Doc::

    https://github.com/rucha80/PDF-Data-Extraction/blob/main/pdf_parsing.py


"""
import os
from typing import List, Union, Dict
import tempfile
import requests

try :
   import pdfkit, pdftotext   
except:
    ss= """pip install pdfkit pdftotext
    conda install -c conda-forge pdftotext
    Html to pdf is also dependent on wkhtmltopdf (i did add exception and info on installation)
    """
    print(ss)
    sys.exit(0)



###############################################################################
def test_all():
    test1()


def test1():
    def do_test(files=None, html=None):
        try:
            html_to_pdf(files, html=html, output_file='test.pdf')
        except Exception as e:
            print(e)
            assert False

    files = ['https://www.google.com', 'https://www.github.com']
    do_test(files)
    test_html = '<h1>test</h1>'
    with open('test.html', 'w') as f:
        f.write(test_html)
    do_test(['test.html',])
    do_test('test.html')
    do_test(html=test_html)
    do_test(files + ['test.html',])

    # print(pdf_to_text('test.pdf'))


###############################################################################
def html_to_pdf(files_links:Union[List, str] = None, 
                html:str=None,
                output_file = 'output.pdf', 
                page_size:str='A4',
                margin_left:str=None,
                margin_right:str=None,
                margin_top:str=None,
                margin_bottom:str=None,
                encoding:str='utf8',
                cookie:Union[Dict,List]=[],
                custom_css_files:List=None,):
    """
    Convert html files to pdf file.

    Doc::
        Args:
            files_links (list or str): list of html files or links or single html file or link
            html (str): instead of file use html string
            output_file (str): output pdf file name
            page_size (str): page size
            margin_left (str): margin left
            margin_right (str): margin right
            margin_top (str): margin top
            margin_bottom (str): margin bottom
            encoding (str): encoding
            cookie (dict or list): cookie [(name, value), ...] or {name: value, ...}
            custom_css_files (list): list of css files
    """

    try:
        config = pdfkit.configuration()
    except OSError:
        raise Exception('wkhtmltopdf not found!\n Download it from https://wkhtmltopdf.org/downloads.html and add it to PATH')

    options = {
        'page-size': page_size,
        'encoding': encoding,
        'cookie': cookie,
    }

    if margin_left:
        options['margin-left'] = margin_left
    if margin_right:
        options['margin-right'] = margin_right
    if margin_top:
        options['margin-top'] = margin_top
    if margin_bottom:
        options['margin-bottom'] = margin_bottom

    if custom_css_files:
        options['-user-style-sheet'] = ''
        options['enable-local-file-access'] = ''

    if cookie:
        req_cookie = {}
        pdfkit_cookie = []
        if isinstance(cookie, list):
            pdfkit_cookie = cookie
            for i, j in cookie:
                req_cookie[i] = j
        elif isinstance(cookie, dict):
            req_cookie = cookie
            for i, j in cookie.items():
                pdfkit_cookie.append((i, j))


    is_file = None
    is_url = None
    mixed = None

    def check_url(url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 OPR/102.0.0.0'
        }
        try:
            r = requests.head(url, headers=headers, allow_redirects=True)
            return bool(r)
        except:
            return False

    if isinstance(files_links, str):
        files_links = [files_links,]
        
    if isinstance(files_links, list):
        for file_link in files_links:
            if os.path.isfile(file_link):
                if is_url:
                    mixed = True
                    is_url = False
                    is_file = False
                    break
                if is_file is None:
                    is_file = True
                    continue
            else:
                if check_url(file_link):
                    if is_file:
                        mixed = True
                        is_url = False
                        is_file = False
                        break
                    if is_url is None:
                            is_url = True
                            continue
                else:
                    raise FileNotFoundError('Invalid file directory or url')


    if is_url:
        pdfkit.from_url(files_links, output_file, options=options)
    elif is_file:
        pdfkit.from_file(files_links, output_file, options=options, css=custom_css_files)
    elif mixed:
        from pypdf import PdfMerger
        merger = PdfMerger()

        for path in files_links:
            # create temp pdf file
            temp = tempfile.NamedTemporaryFile()
            temp_file = temp.name
            temp.close()
            if os.path.isfile(path):
                pdfkit.from_file(path, temp_file, options=options, css=custom_css_files)

            else:
                pdfkit.from_url(path, temp_file, options=options)

            merger.append(temp_file)

        merger.write(output_file)
        merger.close()
    
    elif html:
        pdfkit.from_string(html, output_file, options=options, css=custom_css_files)


def pdf_to_text(pdf_file, password=None, split_by_page=False):
    """
    Convert pdf file to text.

    Doc::
        Args:
            pdf_file (str): pdf file path
            password (str): password for pdf file
            split_by_page (bool): split text by page
    """

    import pdftotext

    with open(pdf_file, "rb") as f:
        pdf = pdftotext.PDF(f, password=password)

    if split_by_page:
        return pdf
    
    return "\n\n".join(pdf)



def pdf_example():
    ss = """
    Created on Wed Oct 28 14:25:28 2020

    @author: 3kt

    path = r'C:\Users\3kt\Downloads\karunyahaloi01.pdf'
    path1 = r"C:\Users\3kt\Downloads\RuchaSawarkar.pdf"
    path2 = r"C:\Users\3kt\Downloads\resume.pdf"

    #Using PyPDF2
    # importing required modules  
    import PyPDF4    
    # creating a pdf file object  
    pdfFileObj = open(path1, 'rb')    
    # creating a pdf reader object  
    pdfReader = PyPDF4.PdfFileReader(pdfFileObj)    
    # printing number of pages in pdf file  
    print(pdfReader.numPages)    
    # creating a page object  
    pageObj = pdfReader.getPage(0)    
    pypdf2_text = pdfReader.getPage(0).extractText()
    # extracting text from page  
    for i in range(pdfReader.numPages):
        pypdf2_text +=pdfReader.getPage(i).extractText()
    #print(pageObj.extractText())    
    # closing the pdf file object  
    pdfFileObj.close()  

    #using Tika
    from tika import parser # pip install tika
    raw = parser.from_file(path)
    tika_text = raw['content']

    import codecs
    #using Textract
    import textract
    textract_text = textract.process(r'C:\Users\3kt\Downloads\karunyahaloi01.pdf')
    textract_str_text = codecs.decode(textract_text)


    #Usinf pymupdf
    import fitz  # this is pymupdf
    with fitz.open(path2) as doc:
        pymupdf_text = ""
        for page in doc:
            pymupdf_text += page.getText()
    #print(pymupdf_text)



    #Using PDFminer
    from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
    from pdfminer.converter import TextConverter
    from pdfminer.layout import LAParams
    from pdfminer.pdfpage import PDFPage
    from io import StringIO

    def convert_pdf_to_txt(path):
        rsrcmgr = PDFResourceManager()
        retstr = StringIO()
        codec = 'utf-8'
        laparams = LAParams()
        device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
        fp = open(path, 'rb')
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        password = ""
        maxpages = 0
        caching = True
        pagenos=set()
        for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
            interpreter.process_page(page)
        text = retstr.getvalue()
        fp.close()
        device.close()
        retstr.close()
        return text

    pdf_miner_text = convert_pdf_to_txt(path2)

    #Using PDFtotext
    import pdftotext
    # Load your PDF
    with open(path1, "rb") as f:
        pdf = pdftotext.PDF(f)
    # Read all the text into one string
    pdftotext_text = "\n\n".join(pdf)
    #print("\n\n".join(pdf))

    def saveText(texto, fileName, nameLib):
        arq = open(fileName + "-" + nameLib + ".txt", "w")
        arq.write(texto)        
        arq.close()
        
    saveText(pdftotext_text, r"C:\Users\3kt\Desktop\Rucha\Similarity\pinku.txt", "pdftotext")


    #using Tabula
    import tabula
    df = tabula.read_pdf(path, pages='all')
    """
    print(ss)

###################################################################################################
if __name__ == "__main__":
    import fire
    fire.Fire()
