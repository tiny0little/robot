#!/usr/bin/env python3

import smbus
import math
import sqlite3

Register_A     = 0                 #Address of Configuration register A
Register_B     = 0x01              #Address of configuration register B
Register_mode  = 0x02              #Address of mode register
X_axis_H       = 0x03              #Address of X-axis MSB data register
Z_axis_H       = 0x05              #Address of Z-axis MSB data register
Y_axis_H       = 0x07              #Address of Y-axis MSB data register
declination    = -0.00669          #define declination angle of location where measurement going to be done
#declination   = 0
pi             = 3.14159265359     #define pi value


def Magnetometer_Init():
        bus.write_byte_data(Device_Address, Register_A, 0x70)
        bus.write_byte_data(Device_Address, Register_B, 0xa0)
        bus.write_byte_data(Device_Address, Register_mode, 0)

def read_raw_data(addr):
        high = bus.read_byte_data(Device_Address, addr)
        low = bus.read_byte_data(Device_Address, addr+1)
        value = ((high << 8) | low)
        if(value > 32768):
          value = value - 65536
        return value


bus = smbus.SMBus(1) 	# or bus = smbus.SMBus(0) for older version boards
Device_Address = 0x1e   # HMC5883L magnetometer device address
Magnetometer_Init()     # initialize HMC5883L magnetometer 

	
x = read_raw_data(X_axis_H)
z = read_raw_data(Z_axis_H)
y = read_raw_data(Y_axis_H)
heading = math.atan2(y, x) + declination
        
if (heading > 2*pi):
  heading = heading - 2*pi

if (heading < 0):
  heading = heading + 2*pi

heading_angle = int(heading * 180/pi)
print(f"heading angle[{heading_angle}]")



con = sqlite3.connect('data.db')
cur = con.cursor()

print('updating DB ...')
cur.execute("DELETE FROM sensors WHERE name='heading'")
cur.execute(f"INSERT INTO sensors VALUES ('heading',{heading_angle})")
con.close()


