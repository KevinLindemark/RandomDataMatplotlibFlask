from random import randint
import sqlite3 as lite
import schedule
from time import sleep
con = lite.connect('database.db')
"""
CREATE TABLE dhtReadings (timestamp DATETIME,  temp NUMERIC, hum NUMERIC);
/* No STAT tables available */
"""
def insertRandomData():
    query = "INSERT INTO dhtReadings (timestamp, temp, hum) VALUES(datetime('now'), ?, ?)"
    temp = randint(10, 40)
    hum = randint(10, 40)
    data = (temp, hum)
    with con:
        cur = con.cursor() 
        cur.execute(query, data)
while True:
    insertRandomData()
    sleep(3)