import sqlite3

class MileageDBManager:
    conn = None
    def __init__(self):
        self.conn = sqlite3.connect('text.db')
        #print("database initiated")

    def isInCityList(self,cityName):
        lst = self.conn.execute("""
            SELECT CITYNAME FROM CITY
        """)
        for a in lst:
            if cityName in a:
                return True
        return False

    def insertNewCity(self,cityName):
        if self.isInCityList(cityName):
            print("False")
            return
        self.conn.execute("""
            INSERT INTO CITY(CITYNAME)
            VALUES (?)
        """,[cityName])
        self.conn.commit()

    def insertNewConnectData(self,cityName1,cityName2,FullMileage,ThreeQuaterMileage,HalfMileage):
        if self.isInConnectList(cityName1,cityName2,FullMileage):
            return
        self.conn.execute("""
            INSERT INTO CONNECT(CITY1,CITY2,MILEAGEFULL,MILEAGE3QUARTER,MILEAGEHALF)
            VALUES (?,?,?,?,?)
        """,[cityName1,cityName2,FullMileage,ThreeQuaterMileage,HalfMileage])
        self.conn.commit()

    def isInConnectList(self,cityName1,cityName2,FullMileage):
        lst = self.conn.execute("""
            SELECT CITY1,CITY2,MILEAGEFULL FROM CONNECT
        """)
        for a in lst:
            if (FullMileage == a[2]) and ((cityName1 in a[0] and cityName2 in a[1]) or (cityName1 in a[1] and cityName2 in a[0])):
                return True
        return False

    def refactorConnList(self):
        connectList = self.conn.execute("""
            SELECT * FROM CONNECT
        """)
        for a in connectList:
            self.conn.execute("""
            UPDATE CONNECT
            SET CITY2 = ?
            WHERE CITY1 = ? AND CITY2 = ? AND MILEAGEFULL = ?
        """,[a[1].lower(),a[0],a[1],a[2]])
        self.conn.commit()

    def refactorCityList(self):
        connectList = self.conn.execute("""
            SELECT *  FROM CONNECT
        """)
        citylist = self.conn.execute("""
            SELECT * FROM CITY
        """)
        for a in connectList:
            lower = a[1].lower()
            self.insertNewCity(lower)

class FlightDBManager:
    conn = None
    def __init__(self):
        self.conn = sqlite3.connect("text.db")

    def insertNewFlight(self,depatureCity, arrivalCity, depatureTime, arrivalTime, mileage, FlightNO):
        if self.flightInDatabase(FlightNO):
            return
        self.conn.execute("""
            INSERT INTO FLIGHT(DEPATURECITY,DESTINATIONCITY,DEPATURETIME,ARRIVALTIME,MILEAGEFULL,FLIGHTNO)
            VALUES (?,?,?,?,?,?)
        """,[depatureCity,arrivalCity,depatureTime,arrivalTime,mileage,FlightNO])
        self.conn.commit()

    def flightInDatabase(self,FlightNO):
        flightlist = self.conn.execute("""
            SELECT * FROM FLIGHT
        """)
        for flight in flightlist:
            if FlightNO in flight:
                return True
        return False

    