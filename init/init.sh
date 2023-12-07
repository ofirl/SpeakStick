#! /bin/bash

# default admin password: SpeakStick4U!
# logs can be viewed here: https://one.eu.newrelic.com/logger

# Run this script after cloning the repository:
# cd /opt
# git clone https://github.com/ofirl/SpeakStick.git
# cd SpeakStick

git config --global --add safe.directory /opt/SpeakStick

sudo apt update
sudo apt upgrade -y

# Installations --- Installations --- Installations --- Installations --- Installations --- Installations --- 
# python libraries
sudo apt-get -y install python3-dev libpython3-all-dev python3-pip sqlite3 libxml2-dev libgirepository1.0-dev libxslt-dev libcairo2-dev libsmbclient-dev libcap-dev
# sudo apt install -y libsdl2-dev libsdl2-mixer-2.0-0 libsdl2-mixer-dev

sudo pyhton3 -m venv /usr/local/bin
sudo pip3 install -r /opt/SpeakStick/requirements.txt
# sudo apt-get -y install python3-pygame

# yarn & node
curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -
echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list
sudo apt update
sudo apt install -y yarn

# node
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt -y install nodejs

# nginx
sudo apt install nginx -y
sudo systemctl start nginx

# Automatic Upgrades --- Automatic Upgrades --- Automatic Upgrades --- Automatic Upgrades --- Automatic Upgrades ---
echo '0 1 * * * speakstickadmin curl localhost:8090/api/upgrade' >> ~/speakstick-upgrade-cron
sudo cp ~/speakstick-upgrade-cron /etc/cron.d/speakstick

# Services --- Services --- Services --- Services --- Services --- Services --- Services --- Services ---
sudo ./init/init_systemctl_services.sh

# First Build --- First Build --- First Build --- First Build --- First Build --- First Build --- First Build ---
# run an upgrade in order to build everything for the first time
./upgrade-script.sh

# Access Point --- Access Point --- Access Point --- Access Point --- Access Point --- Access Point --- Access Point ---
# https://forums.raspberrypi.com//viewtopic.php?t=198946
# https://pimylifeup.com/raspberry-pi-wireless-access-point/

# udev rules
sudo cp /opt/SpeakStick/init/72-wlan-geo-dependent.rules /etc/udev/rules.d/72-wlan-geo-dependent.rules

# installations
sudo apt install hostapd dnsmasq

# dhcpcd config
sudo echo 'interface wlan1
    static ip_address=192.168.220.1/24
    nohook wpa_supplicant' >> /etc/dhcpcd.conf

# hostapd config
sudo cp /opt/SpeakStick/init/hostapd.conf /etc/hostapd/hostapd.conf

echo DAEMON_CONF="/etc/hostapd/hostapd.conf" >> /etc/default/hostapd

# dnsmasq config
sudo cp /etc/dnsmasq.conf /etc/dnsmasq.conf.orig
cat /opt/SpeakStick/init/dnsmasq.conf >> /etc/dnsmasq.conf

# restart services
sudo systemctl restart dhcpcd
sudo systemctl unmask hostapd
sudo systemctl enable hostapd
sudo systemctl start hostapd
sudo systemctl restart dnsmasq

# Bashrc --- Bashrc --- Bashrc --- Bashrc --- Bashrc --- Bashrc --- Bashrc --- Bashrc --- Bashrc ---
# bashrc aliases (for convenient)
cat /opt/SpeakStick/init/aliases.sh >> ~/.bashrc


# --- Audio --- Audio --- Audio --- Audio --- Audio --- Audio --- Audio --- Audio --- Audio --- Audio ---

# SDL_AUDIODRIVER=alsa
# SDL_AUDIODEV=/dev/audio




# Manual Steps --- Manual Steps --- Manual Steps --- Manual Steps --- Manual Steps --- Manual Steps ---

# sudo nano /etc/default/hostapd
# replace: #DAEMON_CONF="" 
# with: DAEMON_CONF="/etc/hostapd/hostapd.conf"

# sudo nano /etc/init.d/hostapd
# replace: DAEMON_CONF= 
# with: DAEMON_CONF=/etc/hostapd/hostapd.conf