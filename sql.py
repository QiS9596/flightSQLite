# import sqlite3
# conn = sqlite3.connect('test.db')
# print("database initiated")
# conn.execute("""
#   DROP TABLE FLIGHT
# """)
# conn.commit()
# conn.close()
import sqlite3
conn = sqlite3.connect('test.sqlite')