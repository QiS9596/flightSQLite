
# import textract
# import codecs
#
# def readPdfToTextInUTF8(pdfPathAsInput, txtNameAsOutput = "output.txt"):
#     text = textract.process(pdfPathAsInput)
#     strResult = text.strip().decode('utf-8')
#     file = codecs.open(txtNameAsOutput,'w','utf-8')
#     file.write(strResult)
#     file.close()
#
# def readPdfToHtml(pdfPathAsInput):
#     pass
#
# file = codecs.open("output.txt","r","utf-8")
# for line in file.readlines():
#     print(line)
# file.close()

#printerr(text)



#subprocess.call(('pdf2htmlEX','ANA domestic.pdf'))

"""
from pdfminer.pdfinterp import PDFResourceManager, process_pdf
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from io import StringIO
def convert_pdf(path, page=1):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, pageno=page,  laparams=laparams)
    fp = open(path, 'rb')
    process_pdf(rsrcmgr, device, fp)
    fp.close()
    device.close()
    str = retstr.getvalue()
    retstr.close()
    return str

file  = r'ANA domestic.pdf'
print(convert_pdf(file))
"""

from bs4 import BeautifulSoup
from bs4 import UnicodeDammit
from urllib.request import urlopen
import re
import sys

def deleteFiles():
    html = open("./ANA domestic.html",encoding='utf-8')
    data = re.sub("(<img).*(\"\/>)","",html.read())
    html.close()
    html = open("./ANA domesticNoPhoto.html",'w',encoding='utf-8')
    html.write(data)
    html.flush()
    html.close()
# html = html.decoding('ascii').encoding('utf-8')
# try:
#     bs = BeautifulSoup(html,"lxml")
# except UnicodeDecodeError as e:
#     print(e.object)
#
def handlePage(page):
    Titles = page.findAll("div",{"class":re.compile("(t m0 .* ffb.*)")})


html = open("./ANA domestic.html",encoding='utf-8')
bs = BeautifulSoup(html,"lxml")
pages = bs.findAll("div",{"class":re.compile("pf(.)*")})
for page in pages:
    handlePage(page)


# for b in a:
#    print(b)