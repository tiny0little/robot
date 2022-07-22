#!/usr/bin/env python3

import board
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import sqlite3
from datetime import datetime
import os
import subprocess


BASE_DIR='/home/pi/src/robot/'

con = sqlite3.connect(f'{BASE_DIR}data.db')
cur = con.cursor()

i2c = board.I2C()
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C)

oled.fill(0)
oled.show()

# Create blank image for drawing.
image = Image.new("1", (oled.width, oled.height))
draw = ImageDraw.Draw(image)

tiny_font = ImageFont.truetype(f"{BASE_DIR}fonts/Quicksand-Regular.ttf", 10)
small_font = ImageFont.truetype(f"{BASE_DIR}fonts/Quicksand-Regular.ttf", 13)
segoe_symbols_font_21 = ImageFont.truetype(f"{BASE_DIR}fonts/Segoe_MDL2_Assets.ttf", 21)
hololens_symbols_font_21 = ImageFont.truetype(f"{BASE_DIR}fonts/HoloLens_MDL2_Assets.ttf", 21)



now = datetime.now()
current_time = now.strftime("%H:%M")
print(f"now[{current_time}]")
load1, load5, load15 = os.getloadavg()

cpu_temperature=int(subprocess.getoutput("cat /sys/class/thermal/thermal_zone0/temp | awk '{ printf(\"%d\",$1/1000) }'"))
print(f"cpu[{cpu_temperature:n}C]")

wifi_signal_level=int(subprocess.getoutput("/usr/sbin/iwconfig wlan0 | grep Signal").split('level=-')[1].split('dBm')[0].strip())
print(f"wifi[{wifi_signal_level:n}dBm]")

if wifi_signal_level>67:
  wifi_signal_display='\uec3d'
elif wifi_signal_level>57:
  wifi_signal_display='\uec3e'
elif wifi_signal_level>47:
  wifi_signal_display='\uec3f'
else:
  wifi_signal_display='\uec3f'


cur.execute('SELECT value FROM sensors WHERE name="temperature"')
temperature = cur.fetchall()[0][0]
cur.execute('SELECT value FROM sensors WHERE name="humidity"')
humidity = cur.fetchall()[0][0]
temperature_display=f"T[{temperature:n}C]"
print(f"temp[{temperature:n}C {humidity:n}%]")

cur.execute('SELECT value FROM sensors WHERE name="batt_voltage"')
batt_voltage = cur.fetchall()[0][0]
cur.execute('SELECT value FROM sensors WHERE name="batt_capacity"')
batt_capacity = cur.fetchall()[0][0]
cur.execute('SELECT value FROM sensors WHERE name="batt_charging"')
batt_charging = cur.fetchall()[0][0]
print(f"batt[{batt_capacity:n}%]")

if batt_charging:
  if batt_capacity > 90:
    batt_display = '\uebb5'
  elif batt_capacity > 80:
    batt_display = '\uebb4'
  elif batt_capacity > 70:
    batt_display = '\uebb3'
  elif batt_capacity > 60:
    batt_display = '\uebb2'
  elif batt_capacity > 50:
    batt_display = '\uebb1'
  elif batt_capacity > 40:
    batt_display = '\uebb0'
  elif batt_capacity > 30:
    batt_display = '\uebaf'
  elif batt_capacity > 20:
    batt_display = '\uebae'
  elif batt_capacity > 10:
    batt_display = '\uebad'
  else:
    batt_display = '\uebab'
else:
  if batt_capacity > 90:
    batt_display = '\uebaa'
  elif batt_capacity > 80:
    batt_display = '\ueba9'
  elif batt_capacity > 70:
    batt_display = '\ueba8'
  elif batt_capacity > 60:
    batt_display = '\ueba7'
  elif batt_capacity > 50:
    batt_display = '\ueba6'
  elif batt_capacity > 40:
    batt_display = '\ueba5'
  elif batt_capacity > 30:
    batt_display = '\ueba4'
  elif batt_capacity > 20:
    batt_display = '\ueba3'
  elif batt_capacity > 10:
    batt_display = '\ueba2'
  else:
    batt_display = '\ue850'


cur.execute('SELECT value FROM sensors WHERE name="heading"')
heading_angle = cur.fetchall()[0][0]
print(f"heading[{heading_angle:n}°]")


draw.text((0, 50), current_time, font=small_font, fill=255)
draw.text((98, 0), batt_display, font=segoe_symbols_font_21, fill=255)
draw.text((109, 19), wifi_signal_display, font=segoe_symbols_font_21, fill=255)


draw.text((0, 0), "\ue9ca", font=segoe_symbols_font_21, fill=255)
draw.text((17, -2), f"{temperature:n}C", font=small_font, fill=255)
draw.text((17, 8), f"{humidity:n}%", font=small_font, fill=255)

draw.text((0, 25),"\ue950", font=segoe_symbols_font_21, fill=255)
draw.text((24, 22), f"{cpu_temperature:n}C", font=small_font, fill=255)
draw.text((24, 34), f"{load1:.2f}", font=small_font, fill=255)

draw.text((43, 0),"\ue942", font=hololens_symbols_font_21, fill=255)
draw.text((65, 1), f"{heading_angle:n}°", font=small_font, fill=255)



oled.image(image)
oled.show()
con.close()

