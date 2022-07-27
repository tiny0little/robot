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
  ./hc-sr04.py
  echo
  ./display.py
  mv robot-screen.png /var/www/html/

  echo
  echo sleeping for 8 sec
  sleep 8
  echo
done


