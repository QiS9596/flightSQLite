import pymysql
from queue import Queue
import SendData2mySQL
import sql
import util
import ssl
from bs4 import BeautifulSoup
from urllib.request import urlopen
import threading
import re


def getAllIllegalData(db):
    cursor = db.cursor()
    sqlCommand = """SELECT * FROM airline
                    WHERE kilos = 0 or kilos = -1 or kilos = \'KILOS\'"""
    cursor.execute(sqlCommand)
    return cursor.fetchall()

def getAllFlightData(db):
    cursor = db.cursor()
    sqlCommand = """SELECT * FROM airline"""
    cursor.execute(sqlCommand)
    return cursor.fetchall()

def getMatchedCity(db,IATA):
    cursor = db.cursor()
    sqlCommand = """SELECT * FROM airport
                    WHERE IATA = \'%s\'"""%IATA
    cursor.execute(sqlCommand)
    a = cursor.fetchall()
    if a == 0 or len(a) == 0:
        raise util.NullResultException("MileageCheck.getMatchedCity: no matched city for airport: "+IATA)
    return a

def getOnlineMileage(IATA1,IATA2):
    url = """http://www.webflyer.com/travel/mileage_calculator/getmileage.php?city=%s&city=%s&city = & city = & city = & city = & bonus = 0 & bonus_use_min = 0 & class_bonus = 0 & class_bonus_use_min = 0 & promo_bonus = 0 & promo_bonus_use_min = 0 & min = 0 & min_type = m & ticket_price = """%(IATA1,IATA2)
    gcontext = ssl._SSLContext(ssl.PROTOCOL_SSLv23)
    html = urlopen(url,context=gcontext)
    bs = BeautifulSoup(html,'lxml')

    warning = bs.find_all('td',{'align':"CENTER",'valign':"TOP"})
    for suggestion in warning:
        temp = suggestion.find('b')
        if temp:
            raise util.QueryException(temp.text+" not recorded in the online mileage calculator")
    rows = bs.find_all("tr",{'class':'row_odd_bg'})
    result = []
    for row in rows:
        datas = row.find_all('td')
        texts = []
        for data in datas:
            texts.append(data.text)
        if 'Distance' in texts:
            print(texts)
            for text in texts:
                if re.match('[0-9\.]+ miles',text):
                    numric = re.sub('miles','',text)
                    result.append(float(numric))
    mileage = 'NULL'
    try:
        mileage = min(result)
    except ValueError:
        print(IATA1+' '+IATA2)
    except TypeError as TE:
        print (TE)
        print(IATA1+ ' ' + IATA2)
    return mileage

communicationQueue = Queue()
_sentinel = object()

def databaseManagerThreadFunc():
    dbm = SendData2mySQL.mySQLFlightManager()
    print("database Manager Thread initiated")
    while True:
        if not communicationQueue.qsize()==0:
            print('communication queue not null, current size is '+ str(communicationQueue.qsize()))
            obj = communicationQueue.get()
            if obj == _sentinel:
                return
            dbm.updateInfo(obj[0],obj[1])

def fillMileageChart():
    db = util.dbinit()
    result = getAllIllegalData(db)
    anaflightdb = sql.MileageDBManager()
    th = threading.Thread(target=databaseManagerThreadFunc)
    th.start()
    i = 0
    j = len(result)
    for data in result:
        i+=1
        global mileage
        mileage = 'NULL'
        #print(data)
        print(str(i)+'/'+str(j))
        try:
            try:
                city1 = getMatchedCity(db, data[1])[0][1].lower()
                city2 = getMatchedCity(db, data[2])[0][1].lower()
                mileage = int(anaflightdb.getMileage(city1,city2))
            except util.NullResultException:
                mileage = getOnlineMileage(data[1],data[2])
            print('start to put data into queue' + str(data[0]) + ' ' + str(mileage))
            communicationQueue.put([data[0],mileage])
            print(communicationQueue.qsize())
        except util.QueryException as qe:
            print('query exception')
            util.logutil('ANAFlightExceptionLog.txt').log(str = str(qe.args),header = str(qe.__class__))
        except IndexError:
            print('index error')
            util.ANAFlightException("Unknow Exception occured for city "+ str(data))
        # except Exception as E:
        #     print(E.__class__)
        #     print(E)

    communicationQueue.put(_sentinel)