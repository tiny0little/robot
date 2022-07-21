#!/usr/bin/env python3

import time
import smbus2
import logging
from ina219 import INA219,DeviceRangeError
import sqlite3


DEVICE_BUS = 1
DEVICE_ADDR = 0x17
PROTECT_VOLT = 3700
SAMPLE_TIME = 2



ina_batt = INA219(0.005, busnum=DEVICE_BUS, address=0x45)
ina_batt.configure()
batt_voltage = ina_batt.voltage()
batt_current = ina_batt.current()
batt_power = ina_batt.power()
if batt_current>0:
  batt_charging=1
  print("Battery is charging")
else:
  batt_charging=0
  print("Battery is not charging")

print("Batteries Voltage: %.2fV" % batt_voltage)


bus = smbus2.SMBus(DEVICE_BUS)
aReceiveBuf = []
aReceiveBuf.append(0x00)
for i in range(1,255):
    aReceiveBuf.append(bus.read_byte_data(DEVICE_ADDR, i))

batt_capacity = (aReceiveBuf[20] << 8 | aReceiveBuf[19])
print("Battery remaining capacity: %d%%"% batt_capacity)



con = sqlite3.connect('data.db')
cur = con.cursor()
print('updating DB ...')

cur.execute("DELETE FROM sensors WHERE name='batt_voltage'")
cur.execute(f"INSERT INTO sensors VALUES ('batt_voltage',{batt_voltage})")
cur.execute("DELETE FROM sensors WHERE name='batt_charging'")
cur.execute(f"INSERT INTO sensors VALUES ('batt_charging',{batt_charging})")
cur.execute("DELETE FROM sensors WHERE name='batt_capacity'")
cur.execute(f"INSERT INTO sensors VALUES ('batt_capacity',{batt_capacity})")


con.commit()
con.close()

