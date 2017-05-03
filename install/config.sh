#!/bin/bash
# Add scripts to boot menu

# Load Chromium after login
sudo ln -s /home/pi/GaragePi/garagepi_web.sh /etc/profile.d/garagepi_web.sh

# Load Python server after login
sudo ln -s /home/pi/GaragePi/garagepi_server.sh /etc/profile.d/garagepi_server.sh
