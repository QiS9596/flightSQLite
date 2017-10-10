import pymysql
import sys

dbName = 'FlightMySql'
usrname = 'admin'
authentication_string = 'admin'
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

db = pymysql.connect('localhost', usrname, authentication_string, dbName)
cursor = db.cursor()
class mySQLFlightManager:
    def __init__(self):
        pass

    def getCityNameList(self):
        """
        get the entire list of cities or airports
        :return: a list or tuple
        """
        pass

    def insertNewFlight(self,depatureCity, arrivalCity, depatureTime, arrivalTime, mileage, FlightNO):
        sql = 'INSERT INTO airline(ID, DepartureAirport, ArriveAirport, DepartureTime, ArriveTime, kilos) VALUES(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')'%(FlightNO,depatureCity,arrivalCity,depatureTime,arrivalTime,mileage)
        cursor.execute(sql)
        db.commit()

    def getAvaliableFlightList(self, depature_city_name):
        """
        get a list of flight that departure from the current city with the name
        :param depature_city_name: the name of the current city
        :return: a list or tuple of flight
        """
        city = depature_city_name.lower()
        sql = 'SELECT * FROM airline WHERE DepartureAirport = \'%s\''%(city)
        cursor.execute(sql)
        query_result = cursor.fetchall()
        result = []
        for flight in query_result:
            result.append([flight[1],flight[2],flight[3],flight[4],flight[5],flight[0]])
        return result

    def flightInDatabase(self, FlightNO):
        """
        check if the current flight is in the flight
        :param FlightNO:the flight number of the flight we want to check
        :return: True is that flight is in the database, False if not
        """
        sql = 'SELECT * FROM airline'
        cursor.execute(sql)
        query_result = cursor.fetchall()
        for flight in query_result:
            if flight[0] == FlightNO:
                return True
        return False


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
