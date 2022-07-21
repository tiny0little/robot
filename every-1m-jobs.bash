#!/usr/bin/bash

cd /home/pi/src/robot


./dht11.py
echo
./ups.py
echo
./display.py


echo
echo sleeping 30 sec
sleep 30

./dht11.py
echo
./ups.py
echo
./display.py

