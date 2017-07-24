
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
    rightShift = False

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
titleTypeRe = re.compile("[A-Z]+(\([A-Z ]+\))?")
flightNoTypeRe = re.compile("[0-9]+")
timeTypeRe = re.compile("([0-9][0-9]):(([0-9][0-9]))")
timeTypeRe2 = re.compile("([0-9][0-9]):(([0-9][0-9]))( )*([0-9][0-9]):(([0-9][0-9]))")
def deleteFiles():
    html = open("./ANA domestic.html",encoding='utf-8')
    #data = re.sub("(<img).*(\"\/>)","",html.read())
    data = re.sub("<div id=\"pf[0-9]*\" class=\"pf w0 h0\" data-page-no=\"([0-9]|10|11|12|13|14|15)*\">.*(</div>)","",html.read())
    html.close()
    html = open("./ANA domesticNoPages.html",'w',encoding='utf-8')
    html.write(data)
    html.flush()
    html.close()

def handlePage(page):
    Titles = page.findAll("div")
    Times = page.findAll("div",{"class":re.compile("(t me .* ffd fs24.*)")})
    FlightNo = page.findAll("div",{"class":re.compile("(t m12 .* ff11 fs17.*)")})

    if Times.__len__()>=1:
        result[page[page_no]] = {}
        result[page[page_no]][titles] = []
        result[page[page_no]][times] = []
        result[page[page_no]][fNo] = []
    else:return
    for title in Titles:
        if titleTypeRe.fullmatch(title.text) and title.text.__len__()>1:
            print(title)
            info = title["class"]
            result[page[page_no]][titles].append(shortedTag(info[2], info[3], info[4], title.text))


    for time in Times:
        if timeTypeRe.fullmatch(time.text):
            info = time["class"]
            result[page[page_no]][times].append(shortedTag(info[2], info[3], info[4], time.text))
        if timeTypeRe2.match(time.text):
            info = time["class"]
            timeInfo = time.text.split(' ')
            result[page[page_no]][times].append(shortedTag(info[2], info[3], info[4], timeInfo[0]))
            st = shortedTag(info[2],info[3],info[4],timeInfo[1])
            st.rightShift = True
            result[page[page_no]][times].append(st)
    for flights in FlightNo:
        if flightNoTypeRe.match(flights.text):
            info = flights["class"]
            result[page[page_no]][fNo].append(shortedTag(info[2], info[3], info[4], flights))

def handleOneType(resultList,rawDataList):
    temp = []
    for a in rawDataList:
        flag = True
        if a.rightShift == False:
            for b in resultList:
                if a.compareTo(b[0],"x")==0:
                    b.append(a)
                    flag = False
            if flag:
                resultList.append([a])
        else:
            temp.append(a)
    for i in range(0, resultList.__len__()):
        min = resultList[i][0].x1
        minidx = i
        for ii in range(i, resultList.__len__()):
            if resultList[ii][0].x1 < min:
                min = resultList[ii][0].x1
                minidx = ii

        a = resultList[i]
        resultList[i] = resultList[minidx]
        resultList[minidx] = a

    if temp.__len__()!=0:
        for element in temp:
            for column in range(0,resultList.__len__()):
                if resultList[column][0].rightShift == False and resultList[column][0].x1 == element.x1:
                    if column+1 < resultList.__len__():
                        resultList[column+1].append(element)
                        break
                    else:
                        resultList.append([element])
                        break
                elif resultList[column][0].rightShift == True and resultList[column][0].x1 == element.x1:
                    resultList[column].append(element)
                    break
    return resultList

def handleResult():
    for p in result.keys():
        handledResult[p] = {}
        for key in result[p].keys():
            handledResult[p][key] = []
        for key in handledResult[p].keys():
            #handledResult[p][key] =
            handleOneType(handledResult[p][key],result[p][key])

def mainProcess():
    html = open("./ANA domestic.html",encoding='utf-8')
    bs = BeautifulSoup(html,"lxml")
    pages = bs.findAll("div",{"class":re.compile("pf(.)*")})
    for page in pages:
        handlePage(page)
    handleResult()


def printResultForTest():
    a = sorted(handledResult.keys())[0]
    print(a)
    for key in handledResult[a].keys():
        print(key)
        print(handledResult[a][key].__len__())
        for array in handledResult[a][key]:
            print(array[0].x1)
            for ele in array:
                print(ele.text)

#mainProcess()
#printResultForTest()
deleteFiles()

# html = open("./ANA domestic.html", encoding='utf-8')
# bs = BeautifulSoup(html,'lxml')
# a = bs.find("div",{"class":"t me xa6 h33 y11cf ffd fs24 fc4 sc0 ls0 ws0"})
# print(a.text)
# print(re.match("([0-9][0-9]):(([0-9][0-9]))( )*([0-9][0-9]):(([0-9][0-9]))",a.text))

