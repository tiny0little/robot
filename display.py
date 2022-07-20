#!/usr/bin/env python3

import board
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import sqlite3
from datetime import datetime
import os



con = sqlite3.connect('data.db')
cur = con.cursor()

i2c = board.I2C()
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C)

oled.fill(0)
oled.show()

# Create blank image for drawing.
image = Image.new("1", (oled.width, oled.height))
draw = ImageDraw.Draw(image)

small_font = ImageFont.truetype("/usr/share/fonts/truetype/piboto/Piboto-Light.ttf", 9)
main_font = ImageFont.truetype("/usr/share/fonts/truetype/piboto/Piboto-Light.ttf", 17)
symbols_font = ImageFont.truetype("HoloLens_MDL2_Assets.ttf", 17)




now = datetime.now()
current_time = now.strftime("%H:%M")
print(f"now=[{current_time}]")
load1, load5, load15 = os.getloadavg()
T_load=f"{load1:.1f}"


cur.execute('SELECT value FROM sensors WHERE name="temperature"')
temperature = cur.fetchall()
cur.execute('SELECT value FROM sensors WHERE name="humidity"')
humidity = cur.fetchall()
T_display=f"T[{temperature[0][0]:n}C]"
print(T_display)

cur.execute('SELECT value FROM sensors WHERE name="batt_voltage"')
batt_voltage = cur.fetchall()[0][0]
cur.execute('SELECT value FROM sensors WHERE name="batt_capacity"')
batt_capacity = cur.fetchall()[0][0]
cur.execute('SELECT value FROM sensors WHERE name="batt_charging"')
batt_charging = cur.fetchall()[0][0]

B_display=f"B[{batt_capacity:n}% {batt_charging:n}]"
print(B_display)



draw.text((102, 0), current_time, font=small_font, fill=255)
draw.text((103, 8), T_load, font=small_font, fill=255)
draw.text((0, 0), T_display, font=main_font, fill=255)
draw.text((0, 17), B_display, font=main_font, fill=255)
draw.text((0, 35), "", font=symbols_font, fill=255)


oled.image(image)
oled.show()
con.close()

