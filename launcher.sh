#!/bin/bash
# launcher.sh
# navigate to home directory, then to this directory, then execute python script, then back home

cd /
cd /home/rsplietho/Documents/iat_kwasten
. /home/rsplietho/Documents/iat_kwasten/.env/bin/activate
sudo python3 main.py
cd /
