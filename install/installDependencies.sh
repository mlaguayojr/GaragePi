#!/bin/bash
# Mario Luis Aguayo Jr.

# Install the needed dependencies for the raspberrypi

clear

echo "[ Installing Dependencies ]\n"

echo "[} Downloading pip"
wget "https://bootstrap.pypa.io/get-pip.py"
python2 get-pip.py

echo "[} Installing Flask"
sudo python2 -m pip install Flask

echo "[} Installing python-mysqldb"
sudo apt-get install python-mysqldb -y

rm get-pip.py
