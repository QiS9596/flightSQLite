
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

#class augmentedList(list):



result = {}
handledResult = {}
page_no = "data-page-no"
titles = "titles"
times = "times"
fNo = "flightNo"
def deleteFiles():
    html = open("./ANA domestic.html",encoding='utf-8')
    data = re.sub("(<img).*(\"\/>)","",html.read())
    html.close()
    html = open("./ANA domesticNoPhoto.html",'w',encoding='utf-8')
    html.write(data)
    html.flush()
    html.close()

def handlePage(page):
    Titles = page.findAll("div",{"class":re.compile("(t m0 .* ffc fs1d.*)")})
    Times = page.findAll("div",{"class":re.compile("(t me .* ffd fs24.*)")})
    FlightNo = page.findAll("div",{"class":re.compile("(t m12 .* ff11 fs17.*)")})

    if Titles.__len__()>=1:
        result[page[page_no]] = {}
        result[page[page_no]][titles] = []
        result[page[page_no]][times] = []
        result[page[page_no]][fNo] = []
    for title in Titles:
        info = title["class"]
        result[page[page_no]][titles].append(shortedTag(info[2], info[3], info[4], title.text))


    for time in Times:
        info = time["class"]
        result[page[page_no]][times].append(shortedTag(info[2], info[3], info[4], title.text))

    for flights in FlightNo:
        info = flights["class"]
        result[page[page_no]][fNo].append(shortedTag(info[2], info[3], info[4], title.text))

def handleOneType(resultList,rawDataList):
    for a in rawDataList:
        flag = True
        for b in resultList:
            if a.compareTo(b[0],"x")==0:
                b.append(a)
                flag = False
        if flag:
            resultList.append([a])
    return resultList

def handleResult():
    for p in result.keys():
        handledResult[p] = {}
        for key in result[p].keys():
            handledResult[p][key] = []
        for key in handledResult[p].keys():
            handledResult[p][key] = handleOneType(handledResult[p][key],result[p][key])


html = open("./ANA domestic.html",encoding='utf-8')
bs = BeautifulSoup(html,"lxml")
pages = bs.findAll("div",{"class":re.compile("pf(.)*")})
for page in pages:
    handlePage(page)
handleResult()
a = sorted(handledResult.keys())[0]
print(a)
for key in handledResult[a].keys():
    print(key)
    print(handledResult[a][key].__len__())
    for array in handledResult[a][key]:
        print(array[0].x1)
        for ele in array:
            print(ele.text)



