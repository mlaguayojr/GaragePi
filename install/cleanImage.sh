#!/bin/bash
# Mario Luis Aguayo Jr.
## Slim down the RPI Image to my liking

clear

# Remove LibreOffice
echo "[Removing Libreoffice]"
sudo apt-get remove libreoffice* -y >/dev/null

# Remove Minecraft
echo "[Removing Minecraft]"
sudo apt-get remove minecraft-pi -y >/dev/null

# Remove Programming IDEs
echo "[Removing Programming IDEs]"
sudo apt-get remove bluej -y >/dev/null
sudo apt-get remove geany -y >/dev/null
sudo apt-get remove greenfoot -y >/dev/null
sudo apt-get remove wolfram-engine -y >/dev/null
sudo apt-get remove nodered -y >/dev/null
sudo apt-get remove scratch -y >/dev/null
sudo apt-get remove sonic-pi -y >/dev/null
sudo apt-get remove sense-hat -y >/dev/null
sudo apt-get remove sense-emu-tools -y >/dev/null
sudo apt-get remove claws-mail -y >/dev/null

# Remove Dependencies
echo "[Removing Python Games]"
sudo rm -R /home/pi/python_games >/dev/null
sudo apt-get autoremove -y >/dev/null
