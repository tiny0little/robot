#!/usr/bin/env python3

import time
import board
import adafruit_dht
import sqlite3


con = sqlite3.connect('data.db')
cur = con.cursor()
dhtDevice = adafruit_dht.DHT11(board.D4, use_pulseio=False)

try:
  print(f"{dhtDevice.temperature:.1f}C / {dhtDevice.humidity}%")

  print('updating DB ...')
  cur.execute("DELETE FROM sensors WHERE name='temperature'")
  cur.execute(f"INSERT INTO sensors VALUES ('temperature',{dhtDevice.temperature})")
  cur.execute("DELETE FROM sensors WHERE name='humidity'")
  cur.execute(f"INSERT INTO sensors VALUES ('humidity',{dhtDevice.humidity})")

  con.commit()

except RuntimeError as error:
  print(error.args[0])

except Exception as error:
  dhtDevice.exit()
  raise error

finally:
  con.close()


