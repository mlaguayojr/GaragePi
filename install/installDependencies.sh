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

# Remember the credentials you wrote for this section
echo "[} Installing MySQL Server"
sudo apt-get install mysql-server -y

# This is where the credentials are needed from the previous step
# Example: mysql -u<username> -p<password>
#          mysql -uroot -proot
# 		The username here is root, and the password is root.
echo "[} Installing GaragePi database"
mysql -uroot -proot -e 'create database garagepi; use garagepi; source garagepi.sql;'

echo "[} Installing PHPMyAdmin"
sudo apt-get install phpmyadmin -y

rm get-pip.py
