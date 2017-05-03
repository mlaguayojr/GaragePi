#!/bin/bash
# Start Chrome at login to GaragePi
DISPLAY=:0 chromium-browser --kiosk --incognito --app="http://localhost:5000/"
