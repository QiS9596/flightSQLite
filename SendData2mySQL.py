import pymysql
import sys
import util

dbName = util.DEFAULT_REMOTE_DATABASE.database_name
usrname = util.DEFAULT_REMOTE_DATABASE.user_name
authentication_string = util.DEFAULT_REMOTE_DATABASE.authentication_string

def uploadAirline(*args):
    """
    pymysql is required to be imported

    if airlineID is already exist in table,
    data will be updated
    if not,
    add new data into table
    """
    Airline_ID= args[0]
    DepartureAirport = args[1]
    ArriveAirport = args[2]
    DepartureTime = args[3]
    ArriveTime = args[4]
    Kilos= args[5]
    ip = 'localhost'
    username = usrname
    userpassword = authentication_string
    dbname = dbName
    db = pymysql.connect(ip, username, userpassword, dbname)
    cursor = db.cursor()
    
    sql='SELECT * FROM %s.airline WHERE %s.airline.ID = %s'%(dbname, dbname, args[0])
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        db.close
        if(len(result)==0):#not in table, add new airline
            print('not in table')
            addData(Airline_ID,DepartureAirport,ArriveAirport,DepartureTime,ArriveTime,Kilos)
        else:#in the table, update data
            print('update old file')
            updateData(Airline_ID,DepartureAirport,ArriveAirport,DepartureTime,ArriveTime,Kilos)
            print('update done')
    except Exception:
        print(sys.exc_info()[0].__cause__(0))
    #db.close
def updateData(*args):
    ip = 'localhost'
    username = usrname
    userpassword = authentication_string
    dbname = dbName
    db = pymysql.connect(ip, username, userpassword, dbname)
    cursor = db.cursor()
    sql = 'UPDATE airline SET DepartureAirport=\'%s\', ArriveAirport=\'%s\', DepartureTime=\'%s\', ArriveTime=\'%s\', kilos=\'%s\' WHERE ID = \'%s\''%(args[1], args[2],args[3],args[4],args[5],args[0])
    cursor.execute(sql)
    db.commit()
    db.close()

def addData(*args):
    ip = 'localhost'
    username = usrname
    userpassword = authentication_string
    dbname = dbName
    db = pymysql.connect(ip, username, userpassword, dbname)
    cursor = db.cursor()
    sql = 'INSERT INTO airline(ID, DepartureAirport, ArriveAirport, DepartureTime, ArriveTime, kilos) VALUES(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')'%(args[0],args[1],args[2],args[3],args[4],args[5])
    cursor.execute(sql)
    db.commit()
    db.close()

#uploadAirline('05001', 'LOS', 'TPE', '18:00', '19:00', '30')
db = util.dbinit()
cursor = db.cursor()
class mySQLFlightManager:
    def __init__(self):
        pass
    lock = False
    def getCityNameList(self):
        """
        get the entire list of cities or airports
        :return: a list or tuple
        """
        pass

    def insertNewFlight(self,depatureCity, arrivalCity, depatureTime, arrivalTime, mileage, FlightNO):
        while self.lock:
            pass
        self.lock = True
        sql = 'INSERT INTO airline(ID, DepartureAirport, ArriveAirport, DepartureTime, ArriveTime, kilos) VALUES(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')'%(FlightNO,depatureCity,arrivalCity,depatureTime,arrivalTime,mileage)
        cursor.execute(sql)
        db.commit()
        self.lock = False

    def getAvaliableFlightList(self, depature_city_name):
        """
        get a list of flight that departure from the current city with the name
        :param depature_city_name: the name of the current city
        :return: a list or tuple of flight
        """
        while self.lock:
            pass
        self.lock = True

        city = depature_city_name.lower()
        sql = 'SELECT * FROM airline WHERE DepartureAirport = \'%s\''%(city)
        cursor.execute(sql)
        query_result = cursor.fetchall()
        result = []
        for flight in query_result:
            result.append([flight[1],flight[2],flight[3],flight[4],flight[5],flight[0]])
        self.lock = False
        return result

    def flightInDatabase(self, FlightNO):
        """
        check if the current flight is in the flight
        :param FlightNO:the flight number of the flight we want to check
        :return: True is that flight is in the database, False if not
        """
        while self.lock:
            pass
        self.lock = True

        sql = 'SELECT * FROM airline'
        cursor.execute(sql)
        query_result = cursor.fetchall()
        for flight in query_result:
            if flight[0] == FlightNO:
                self.lock = False
                return True
        self.lock = False
        return False

    def updateInfo(self,ID, kilos):
        while self.lock:
            pass
        self.lock = True

        sql = """UPDATE airline SET kilos = %s WHERE ID = \'%s\'"""%(str(kilos),ID)
        print(sql)
        cursor.execute(sql)
        db.commit()
        self.lock = False

    def uploadPhilippineMileage(self,IATA1,IATA2,Mileage):
        while self.lock:
            pass
        self.lock = True
        try:
            self.lock = False
            self.checkPhilippineMileage(IATA1,IATA2)

            return
        except util.NullResultException:
            self.lock = True
            sql = """INSERT INTO MileagePhilippine(IATA1,IATA2,Mileage) VALUES(\'%s\',\'%s\',%d)""" % (IATA1,IATA2,Mileage)
            cursor.execute(sql)
            db.commit()
            self.lock = False

    def checkPhilippineMileage(self,IATA1,IATA2):
        while self.lock:
            pass
        self.lock = True
        sql = """SELECT * FROM MileagePhilippine WHERE IATA1 = \'%s\' AND IATA2 = \'%s\' """%(IATA1,IATA2)
        sql2 = """SELECT * FROM MileagePhilippine WHERE IATA1 = \'%s\' AND IATA2 = \'%s\' """%(IATA2,IATA1)
        cursor.execute(sql)
        query_result = cursor.fetchall()
        cursor.execute(sql2)
        query_result += cursor.fetchall()
        if len(query_result) == 0:
            self.lock = False
            raise util.NullResultException
        self.lock = False
        return query_result[0][2]



class City_Airport_mySQLManager:
    table_name = 'CITY_AIRPORT'
    def insert_new_pair(self,Municipality, Prefecture, ICAO, IATA):
        try:
            sql = 'INSERT INTO CITY_AIRPORT(Municipality,Prefecture,ICAO,IATA) VALUES (\'%s\',\'%s\',\'%s\',\'%s\')'\
                  %(Municipality,Prefecture,ICAO,IATA)
            cursor.execute(sql)
            db.commit()
        except UnicodeError as UE:
            print(str(type(UE)) + UE.__str__())

    def check_existence(self,city_name,ICAL,IATA):
        pass

class MileageDBManager():
    def __init__(self):
        pass