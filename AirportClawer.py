from bs4 import BeautifulSoup
from urllib.request import urlopen
import ssl
import re
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
    for element in row.find_all('td'):

        anchors = element.find_all('a')
        """
        we find that in the table, all city name are stored in the format of:
        <td><a href="/wiki/[a-zA-Z]+_Prefecture" title="[a-zA-Z]+ Prefecture">[a-zA-Z]+</td>
        so we find anchors in table data with title, and that title should be like city_name Prefecture
        """
        if len(data) ==0:
            for anchor in anchors:
                try:
                    if (re.match(pattern='.*Prefecture',string=anchor['title'])
                        or re.match(pattern='[a-zA-Z]+,.+',string=anchor['title'])
                        or anchor['title'] in strange_list):
                        print("an"+anchor.get_text())
                        data.append(anchor.get_text())
                        break

                except KeyError:
                    continue
        """
        We than find that the ICAO standard abbr for airport is always a four upper class char string hold in a <td> tag
        with out any children tags. and the IATA standard abbr for airport is always a three upper class char string
        hold in a <td> tag with out any children tags. We use regex to match these tags
        """
        if len(anchors) == 0:
            possible_abbr = element.get_text()
            if re.match(pattern='[A-Z][A-Z][A-Z][A-Z]$',string=possible_abbr)and len(data) == 1:
                print(possible_abbr)
                data.append(possible_abbr)
            if re.match(pattern='[A-Z][A-Z][A-Z]$',string=possible_abbr) and len(data) == 2:
                print(possible_abbr)
                data.append(possible_abbr)
    try:
        print(data)
        if len(data) == 3:
            dbm.insert_new_pair(data[0],data[1],data[2])
        if len(data) == 2:
            dbm.insert_new_pair(data[0],data[1],"")
    except IndexError:
        continue



