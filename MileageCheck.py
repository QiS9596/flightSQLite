import pymysql
import util

speical_case={"hokkaido":"sapporo","aichi":"nagoya","nakashibetsu":"nemuro nakashibetsu","ishikawa":"komatsu",'yamaguchi':'yamaguchi ube'}

def dbinit(databaseinfo=util.DEFAULT_REMOTE_DATABASE):
    db = pymysql.connect(databaseinfo.host,
                         databaseinfo.user_name,
                         databaseinfo.authentication_string,
                         databaseinfo.database_name)
    return db

def getAllIllegalData(db):
    cursor = db.cursor()
    sqlCommand = """SELECT * FROM airline
                    WHERE kilos = 0"""
    cursor.execute(sqlCommand)
    return cursor.fetchall()

def getMatchedCity(db,IATA):
    cursor = db.cursor()
    sqlCommand = """SELECT * FROM airport
                    WHERE IATA = \'%s\'"""%IATA
    cursor.execute(sqlCommand)
    return cursor.fetchall()

#def updateData(db, )

