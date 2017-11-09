import sqlite3
import random
import util
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

    def getMileage(self,cityName1, cityName2):
        lst = self.conn.execute("""
          SELECT CITY1, CITY2, MILEAGEFULL FROM CONNECT
        """)
        for a in lst:
            if cityName1 in a and cityName2 in a:
                return a[2]
        raise util.NullResultException()

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
