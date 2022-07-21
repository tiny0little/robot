#!/usr/bin/bash

cd /home/pi/src/robot


./hmc5883l.py
echo
./dht11.py
echo
./ups.py
echo
./display.py


echo
echo sleeping 30 sec
sleep 30

./hmc5883l.py
echo
./dht11.py
echo
./ups.py
echo
./display.py

