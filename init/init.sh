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

# SpeakStick service
cp ./speakstick.service /usr/lib/systemd/system/speakstick.service
sudo systemctl daemon-reload
sudo systemctl enable speakstick

# SpeakStick management server service
cp ./speakstick-management-server.service /usr/lib/systemd/system/speakstick-management-server.service
sudo systemctl daemon-reload
sudo systemctl enable speakstick-management-server

# bashrc
echo 'alias ss-logs="sudo journalctl -u speakstick"' >> ~/.bashrc
echo 'alias ss-server-logs="sudo journalctl -u speakstick-management-server"' >> ~/.bashrc
echo 'alias ss-restart="sudo systemctl restart speakstick speakstick-management-server"'  >> ~/.bashrc

echo 'alias cdss="cd /opt/SpeakStick"' >> ~/.bashrc
echo 'alias ss-update="git pull && ss-restart && echo "service restarted"' >> ~/.bashrc



# SDL_AUDIODRIVER=alsa
# SDL_AUDIODEV=/dev/audio


# manual steps:
# 1. change those lines in '/etc/nginx/sites-enabled/default':
# root /var/www/html; -> root /opt/SpeakStick/management-console/dist;
# server_name _; -> server_name speakstick.local;

# add a new location to nginx config:
# location /api {
#   proxy_pass http://localhost:8080;
# }

# convert files to .wav
# https://cloudconvert.com/