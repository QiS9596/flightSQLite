import sqlite3
import random
import datetime
class MileageDBManager:
    """
    Database Manager for maintaining a sqlite database table for Mileage infomation
    """
    conn = None
    def __init__(self):
        self.conn = sqlite3.connect('text.db')

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


class FlightTestingDBManager:
    """
    Use to maintain a temporary sqlite database table for flighte,
    capable for generating random flight for algorithm tests
    """
    conn = None
    def __init__(self):
        self.conn = sqlite3.connect("text.db")

    def getCityNameList(self):
        citylist = self.conn.execute("""
            SELECT CITYNAME FROM CITY
        """)
        return citylist

    def insertNewFlight(self,depatureCity, arrivalCity, depatureTime, arrivalTime, mileage, FlightNO):
        if self.flightInDatabase(FlightNO):
            return
        self.conn.execute("""
            INSERT INTO FLIGHT(DEPATURECITY,DESTINATIONCITY,DEPATURETIME,ARRIVALTIME,MILEAGEFULL,FLIGHTNO)
            VALUES (?,?,?,?,?,?)
        """,[depatureCity,arrivalCity,depatureTime,arrivalTime,mileage,FlightNO])
        self.conn.commit()

    def getAvaliableFlightList(self,depature_city_name):
        city = depature_city_name.lower()
        return self.conn.execute("""
            SELECT * FROM FLIGHT
            WHERE DEPATURECITY = ?
        """,[city])

    def flightInDatabase(self,FlightNO):
        flightlist = self.conn.execute("""
            SELECT * FROM FLIGHT
        """)
        for flight in flightlist:
            if FlightNO in flight:
                return True
        return False

    def randomGenarateFlight(self,num,startFlightNO):
        """
        Call this method to generate random flights and insert them into sql
        will generate journey to and fro
        :param num: the number of flights you want to generate
        :param startFlightNO: the start of the flightNO, the flightNO increases for the following flights
        :return:
        """
        connect = list(self.conn.execute("""
            SELECT * FROM CONNECT
        """))
        for a in range(0,num):
            rand = random.randint(0,connect.__len__()-1)
            dephour = random.randint(0,24-1)
            depmin = random.randint(0,6-1)*10
            hoursec = random.randint(0,5)
            arrhour = (dephour + hoursec)%24
            arrmin = random.randint(0,6-1)*10
            depature_time = DateStringGenerator.numToDateStr(dephour,depmin)
            arrival_time = DateStringGenerator.numToDateStr(arrhour,arrmin)
            depature_city = connect[rand][0]
            arrival_city = connect[rand][1]
            mileage = connect[rand][2]
            FlightNO = startFlightNO+a*2
            self.insertNewFlight(depature_city,arrival_city,depature_time,arrival_time,mileage,FlightNO)
            dephour = random.randint(0,24-1)
            depmin = random.randint(0,6-1)*10
            arrhour = (dephour+hoursec)%24
            arrmin = random.randint(0,6-1)*10
            depature_time = DateStringGenerator.numToDateStr(dephour,depmin)
            arrival_time = DateStringGenerator.numToDateStr(arrhour,arrmin)
            depature_city,arrival_city = arrival_city,depature_city
            FlightNO = FlightNO+1
            self.insertNewFlight(depature_city,arrival_city,depature_time,arrival_time,mileage,FlightNO)
            self.insertNewFlight(depature_city,arrival_city,depature_time,arrival_time,mileage,FlightNO)

class DateStringGenerator:
    @staticmethod
    def numToDateStr(hour,min):
        if hour in range(0,24):
            if min in range(0,60):
                if hour in range(0,10):
                    result = "0"+str(hour)+":"
                else:
                    result = str(hour)+":"
                if min in range(0,10):
                    result = result + "0" + str(min)
                else:
                    result = result + str(min)
                return result

    @staticmethod
    def earlyThan(time1,time2):
        time1 = time1.split(":")
        time2 = time2.split(":")
        if time1[0]<time2[0]:
            return True
        elif time1[0] == time2[0] and time1[1]<time2[1]:
            return True
        else: return False

    @staticmethod
    def toDateObject(time,year,month,day):
        date_str = str(year)+"-"+str(month)+"-"+str(day)+" "+time
        return datetime.datetime.strptime(date_str,"%Y-%m-%d %H:%M")