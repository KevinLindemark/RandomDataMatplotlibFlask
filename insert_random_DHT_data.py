from random import randint
import sqlite3 as lite
import schedule
from time import sleep
con = lite.connect('database.db', check_same_thread=False)
"""
CREATE TABLE dhtReadings (timestamp DATETIME,  temp NUMERIC, hum NUMERIC);
/* No STAT tables available */
"""
def insert_random_data():
    query = "INSERT INTO dhtReadings (timestamp, temp, hum) VALUES(datetime('now'), ?, ?)"
    temp = randint(10, 40)
    hum = randint(10, 40)
    data = (temp, hum)
    with con:
        cur = con.cursor() 
        cur.execute(query, data)

def run():
    while True:
        insert_random_data()
        sleep(3)
