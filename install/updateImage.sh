#!/bin/bash
# Mario Luis Aguayo Jr.
# Update Raspberry Pi Image to the latest release
# Need internet to do so

clear

echo "[Updating Repos]"
sudo apt-get clean
sudo apt-get update

echo "[Installing Updates]"
sudo apt-get upgrade -y
sudo apt-get dist-upgrade -y

