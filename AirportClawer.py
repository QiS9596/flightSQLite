from bs4 import BeautifulSoup
from urllib.request import urlopen
import ssl
import re

gcontext = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
html = urlopen('https://en.wikipedia.org/wiki/List_of_airports_in_Japan',context=gcontext)
bs = BeautifulSoup(html, 'lxml')
#table is the table that contains the data
table = bs.find("table",{"class":"wikitable sortable"})
for row in table.find_all('tr'):
    for element in row.find_all('td'):
        anchors = element.find_all('a')
        """
        we find that in the table, all city name are stored in the format of:
        <td><a href="/wiki/[a-zA-Z]+_Prefecture" title="[a-zA-Z]+ Prefecture">[a-zA-Z]+</td>
        so we find anchors in table data with title, and that title should be like city_name Prefecture
        """
        for anchor in anchors:
            try:
                if re.match(pattern='.*Prefecture',string=anchor['title']):
                    print(anchor.get_text())
            except KeyError:
                continue
        """
        We than find that the ICAO standard abbr for airport is always a four upper class char string hold in a <td> tag
        with out any children tags. and the IATA standard abbr for airport is always a three upper class char string
        hold in a <td> tag with out any children tags. We use regex to match these tags
        """
        if len(anchors) == 0:
            possible_abbr = element.get_text()
            if re.match(pattern='[A-Z][A-Z][A-Z][A-Z]$',string=possible_abbr):
                print(possible_abbr)
            if re.match(pattern='[A-Z][A-Z][A-Z]$',string=possible_abbr):
                print(possible_abbr)

