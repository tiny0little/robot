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

con = sqlite3.connect('data.db')
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
symbols_font = ImageFont.truetype(f"{BASE_DIR}fonts/Segoe_MDL2_Assets.ttf", 31)




now = datetime.now()
current_time = now.strftime("%H:%M")
print(f"now[{current_time}]")
load1, load5, load15 = os.getloadavg()

cpu_temperature=int(subprocess.getoutput("cat /sys/class/thermal/thermal_zone0/temp | awk '{ printf(\"%d\",$1/1000) }'"))
print(f"cpu[{cpu_temperature:n}C]")

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
    batt_display = '\ue862'
  elif batt_capacity > 80:
    batt_display = '\ue861'
  elif batt_capacity > 70:
    batt_display = '\ue860'
  elif batt_capacity > 60:
    batt_display = '\ue85f'
  elif batt_capacity > 50:
    batt_display = '\ue85e'
  elif batt_capacity > 40:
    batt_display = '\ue85d'
  elif batt_capacity > 30:
    batt_display = '\ue85c'
  elif batt_capacity > 20:
    batt_display = '\ue85b'
  else:
    batt_display = '\ue85a'
else:
  if batt_capacity > 90:
    batt_display = '\ue859'
  elif batt_capacity > 80:
    batt_display = '\ue858'
  elif batt_capacity > 70:
    batt_display = '\ue857'
  elif batt_capacity > 60:
    batt_display = '\ue856'
  elif batt_capacity > 50:
    batt_display = '\ue855'
  elif batt_capacity > 40:
    batt_display = '\ue854'
  elif batt_capacity > 30:
    batt_display = '\ue853'
  elif batt_capacity > 20:
    batt_display = '\ue852'
  else:
    batt_display = '\ue850'



draw.text((95, 50), current_time, font=small_font, fill=255)
draw.text((100, -9), batt_display, font=symbols_font, fill=255)
#draw.text((83, 2), f"{batt_capacity:n}%", font=tiny_font, fill=255)

draw.text((0, 0), "\ue9ca", font=symbols_font, fill=255)
draw.text((23, 0), f"{temperature:n}C", font=small_font, fill=255)
draw.text((23, 13), f"{humidity:n}%", font=small_font, fill=255)

draw.text((0, 33),"\ue950", font=symbols_font, fill=255)
draw.text((33, 33), f"{cpu_temperature:n}C", font=small_font, fill=255)
draw.text((33, 45), f"{load1:.2f}", font=small_font, fill=255)


oled.image(image)
oled.show()
con.close()

