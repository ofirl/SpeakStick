#! /bin/bash

sudo apt update
sudo apt upgrade

# python libraries
sudo apt-get -y install python3-pip
sudo pip3 install adafruit-blinka
sudo pip3 install adafruit-circuitpython-mcp3xxx
sudo apt-get -y install python3-pygame

# yarn & node
curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -
echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list
sudo apt update
sudo apt install -y yarn

# node
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt -y install nodejs



# manual steps:
# 1. change those lines in '/etc/nginx/sites-enabled/default':
# root /var/www/html; -> root /opt/SpeakStick/management-console/dist;
# server_name _; -> server_name speakstick.local;

# https://cloudconvert.com/