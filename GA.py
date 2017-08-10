import BFS
import sql
from random import randint
import datetime

class Node:
    """
    Node class for Genetic Algorithm,
    generate a table for each day
    Each table contains an entity for each flight and a bool value representing wether to take it
    """
    def __init__(self, startDate, endDate):
        self.startDate = startDate
        self.endDate = endDate
        self.tables = []
        for i in range(0,(self.endDate-self.startDate).days+1):
            self.tables.append(self.table(self.startDate+datetime.timedelta(days = i)))

    def printInfo(self):
        for a in self.tables:
            print(a.getTableDate())

    def eval(self):
        pass

    class table:

        def __init__(self,currentDate):
            self.currentDate = currentDate
            flights = sql.FlightDBManager().getEntireFlightList()
            self.flightTable = []
            for f in flights:
                flight = BFS.flight(f[2],f[3],f[5],f[4],f[1],f[0],currentDate)
                self.flightTable.append(self.tableElement(flight,randint(0,1)))
        def eval(self):
            pass
        def getTableDate(self):
            return self.currentDate
        def getStartCity(self):
            pass
        def getFinalCity(self):
            pass
        def getFirstDepatureTime(self):
            pass
        def getLastDepatureTime(self):
            pass
        def test(self):
            for f in self.flightTable:
                print(f.flight.flightNO)
                print(f.taken)
        def compareTableElements(self,other):
            for a in range(0, self.flightTable.__len__()):
                print(self.flightTable[a].flight.flightNO)
                print(other.flightTable[a].flight.flightNO)

        class tableElement:
            flight = None
            taken = False
            def __init__(self, flight, taken):
                self.flight = flight
                self.taken = taken

