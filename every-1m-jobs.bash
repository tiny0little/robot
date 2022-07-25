#!/usr/bin/bash

cd /home/pi/src/robot


for i in 1 2 3 4 5 6
do
  ./hmc5883l.py
  echo
  ./dht11.py
  echo
  ./ups.py
  echo
  ./display.py

  echo
  echo sleeping for 8 sec
  sleep 8
  echo
done


