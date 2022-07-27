#!/usr/bin/env python3


from gpiozero import DistanceSensor
from time import sleep
import sqlite3


con = sqlite3.connect('data.db')
cur = con.cursor()

sensor = DistanceSensor(echo=19, trigger=26)
distance = sensor.distance * 100
if distance > 99:
  distance = 99

print('updating DB ...')
cur.execute("DELETE FROM sensors WHERE name='distance'")
cur.execute(f"INSERT INTO sensors VALUES ('distance',{distance})")
con.commit()

con.close()


