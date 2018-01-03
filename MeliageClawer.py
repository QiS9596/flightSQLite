from bs4 import BeautifulSoup
from urllib.request import urlopen
import ssl
import sql
import re
"""
*"Tokyo" is used to indicate both Haneda and Narita airports while "Osaka" is used to indicate Itami, Kansai, and Kobe airports.
"""
def ANAMileage():
    gcontext = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    html = urlopen("https://www.ana.co.jp/wws/us/e/asw_common/amc/reference/tameru/flightmile/dom/chart.html",context=gcontext)
    bs = BeautifulSoup(html,"lxml")
    cities = bs.findAll("div",{"class":"toggle-box"})
    DBM = sql.MileageDBManager()
    for city in cities:
        print(city["id"])
        DBM.insertNewCity(city["id"])
        temp = city.findAll("tr")
        for a in temp:
            data = list(a.findAll("td"))
            if not data.__len__() == 0:
                fullMileage = int(re.sub(",","",data[1].text),10)
                threequaterMileage = int(0.75*fullMileage)
                halfMileage = int(0.5*fullMileage)

                DBM.insertNewConnectData(city["id"],data[0].text.lower(),fullMileage,threequaterMileage,halfMileage)

def PhilippineAirline():
    """
    claw data from https://www.mabuhaymiles.com/EarningMilesFromFlights/ANA-Domestic-Accrual
    and send them into
    :return:
    """
    gcontext = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    html = urlopen(" https://www.mabuhaymiles.com/EarningMilesFromFlights/ANA-Domestic-Accrual",context=gcontext)
    bs = BeautifulSoup(html,'lxml')
    tablebody = bs.find("tbody")
    rows = tablebody.findAll(['tr'])
    print(rows)
    for row in rows:
        dataelements = list(row.findAll('td'))
        if len(dataelements) == 8:
            if len(dataelements[0].string) == len(dataelements[2].string) == 3:
                print(dataelements[0].string + ' ' + dataelements[2].string + ' ' + dataelements[4].string)

PhilippineAirline()