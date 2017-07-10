
#subprocess.call(('pdf2htmlEX','ANA domestic.pdf'))


from bs4 import BeautifulSoup
from bs4 import UnicodeDammit
from urllib.request import urlopen
import re
import sys

class shortedTag:
    def __init__(self,x1,y1,y2,text):
        if(type(x1) ==  type("")):
            self.x1 = int(x1[1:x1.__len__()],16)
            self.y1 = int(y1[1:y1.__len__()],16)
            self.y2 = int(y2[1:y2.__len__()],16)
        self.text = text

    x1 = None
    y1 = None
    y2 = None
    text = None

    def compareTo(self, other, flag):
        if flag == "x":
            return self.x1-other.x1
        if flag == "y":
            return self.y2-other.y2

    def getValue(self,flag):
        if flag == "x":
            return self.x1
        if flag == "y":
            return self.y2

    @staticmethod
    def sortShortedTagList(list,flag):
        for index in range(0,list.__len__()):
            minidx = index
            min = list[index].getValue(flag)
            for indexa in range(index, list.__len__()):
                if list[indexa].getValue(flag)<min:
                    minidx = indexa
                    min = list[minidx].getValue(flag)
            temp = list[index]
            list[index] = list[min]
            list[min] = temp
        return list




result = {}
handledResult = {}
def deleteFiles():
    html = open("./ANA domestic.html",encoding='utf-8')
    data = re.sub("(<img).*(\"\/>)","",html.read())
    html.close()
    html = open("./ANA domesticNoPhoto.html",'w',encoding='utf-8')
    html.write(data)
    html.flush()
    html.close()

def handlePage(page):
    Titles = page.findAll("div",{"class":re.compile("(t m0 .* ffb fs25.*)")})
    Times = page.findAll("div",{"class":re.compile("(t me .* ffd fs24.*)")})
    if Titles.__len__()>=1:
        result[page["data-page-no"]] = {}
        result[page["data-page-no"]]["titles"] = []
        result[page["data-page-no"]]["times"] = []
    for title in Titles:
        #print(title)
        info = title["class"]

        result[page["data-page-no"]]["titles"].append(shortedTag(info[2],info[3],info[4],title.text))


    for time in Times:
        info = time["class"]
        result[page["data-page-no"]]["times"].append(shortedTag(info[2],info[3],info[4],title.text))



html = open("./ANA domestic.html",encoding='utf-8')
bs = BeautifulSoup(html,"lxml")
pages = bs.findAll("div",{"class":re.compile("pf(.)*")})
for page in pages:
    handlePage(page)
for a in result.keys():
    handledResult[a] = {}
    #handledResult[a]["Titles"] = []



