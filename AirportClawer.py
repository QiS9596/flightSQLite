from bs4 import BeautifulSoup
from urllib.request import urlopen
import ssl
import SendData2mySQL

class myException(Exception):
    pass

dbm = SendData2mySQL.City_Airport_mySQLManager()
gcontext = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
html = urlopen('https://en.wikipedia.org/wiki/List_of_airports_in_Japan',context=gcontext)
bs = BeautifulSoup(html, 'lxml')
#table is the table that contains the data
table = bs.find("table",{"class":"wikitable sortable"})
strange_list = ['Asahikawa, Hokkaidō','Tokyo','Chitose, Hokkaidō','Hakodate, Hokkaidō','Kushiro, Hokkaidō','Obihiro, Hokkaidō']
for row in table.find_all('tr'):
    data = []
    """
    we find that in all table rows, the Municipality should show up in the first table data's anchor text
    the Prefecture should be in the second table data's anchor text
    ICAO abbr should be in the fourth table data
    IATA should be in the fifth table data
    """
    elements = row.find_all('td')
    try:
        if not elements[5] == 'Closed':
            dbm.insert_new_pair(elements[0].a.get_text(),elements[1].a.get_text(),elements[3].get_text(),elements[4].get_text())
    except IndexError:
        continue


