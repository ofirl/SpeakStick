#! /bin/bash

# Run this script after cloning the repository:
# cd /opt
# git clone https://github.com/ofirl/SpeakStick.git
# cd SpeakStick

sudo apt update
sudo apt upgrade

# Installations --- Installations --- Installations --- Installations --- Installations --- Installations --- 
# python libraries
sudo apt-get -y install python3-pip
# sudo apt install -y libsdl2-dev libsdl2-mixer-2.0-0 libsdl2-mixer-dev
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

# Automatic Upgrades --- Automatic Upgrades --- Automatic Upgrades --- Automatic Upgrades --- Automatic Upgrades ---
echo '0 1 * * * speakstickadmin curl localhost:8090/api/upgrade' >> ~/speakstick-upgrade-cron
sudo cp ~/speakstick-upgrade-cron /etc/cron.d/speakstick

# Services --- Services --- Services --- Services --- Services --- Services --- Services --- Services ---
# SpeakStick service
cp ./init/speakstick.service /usr/lib/systemd/system/speakstick.service
sudo systemctl daemon-reload
sudo systemctl enable speakstick

# SpeakStick management server service
cp ./init/speakstick-management-server.service /usr/lib/systemd/system/speakstick-management-server.service
sudo systemctl daemon-reload
sudo systemctl enable speakstick-management-server

# Network services
cp ./init/restart-network-services.service /usr/lib/systemd/system/restart-network-services.service
sudo systemctl daemon-reload
sudo systemctl enable restart-network-services

# First Build --- First Build --- First Build --- First Build --- First Build --- First Build --- First Build ---
# run an upgrade in order to build everything for the first time
./upgrade-script.sh

# Access Point --- Access Point --- Access Point --- Access Point --- Access Point --- Access Point --- Access Point ---
# https://forums.raspberrypi.com//viewtopic.php?t=198946
# https://pimylifeup.com/raspberry-pi-wireless-access-point/

# udev rules
sudo echo '#
# +---------------+
# | wlan1 | wlan2 |
# +-------+-------+
# | wlan3 | wlan4 |
# +---------------+ (RPI USB ports with position dependent device names for up to 4 optional wifi dongles)
# 
# | wlan0 | (onboard wifi)
#
ACTION=="add", SUBSYSTEM=="net", SUBSYSTEMS=="usb",  KERNELS=="1-1.2",       NAME="wlan1"
ACTION=="add", SUBSYSTEM=="net", SUBSYSTEMS=="usb",  KERNELS=="1-1.4",       NAME="wlan2"
ACTION=="add", SUBSYSTEM=="net", SUBSYSTEMS=="usb",  KERNELS=="1-1.3",       NAME="wlan3"
ACTION=="add", SUBSYSTEM=="net", SUBSYSTEMS=="usb",  KERNELS=="1-1.5",       NAME="wlan4"' >> /etc/udev/rules.d/72-wlan-geo-dependent.rules

# installations
sudo apt install hostapd dnsmasq

# dhcpcd config
sudo echo 'interface wlan1
    static ip_address=192.168.220.1/24
    nohook wpa_supplicant' >> /etc/dhcpcd.conf

# hostapd config
sudo echo '# Set the channel (frequency) of the host access point
channel=4
# Set the SSID broadcast by your access point (replace with your own, of course)
ssid=speakstick-ctl
# This sets the passphrase for your access point (again, use your own)
wpa_passphrase=SpeakStickConfig4U!
# This is the name of the WiFi interface we configured above
interface=wlan1
# Use the 2.4GHz band (I think you can use in ag mode to get the 5GHz band as well, but I have not tested this yet)
hw_mode=g
# Accept all MAC addresses
macaddr_acl=0
# Use WPA authentication
auth_algs=1
# Require clients to know the network name
ignore_broadcast_ssid=0
# Use WPA2
wpa=2
# Use a pre-shared key
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP
driver=nl80211
# I commented out the lines below in my implementation, but I kept them here for reference.
# Enable WMM
#wmm_enabled=1
# Enable 40MHz channels with 20ns guard interval
#ht_capab=[HT40][SHORT-GI-20][DSSS_CCK-40]' >> /etc/hostapd/hostapd.conf

# dnsmasq config
sudo cp /etc/dnsmasq.conf /etc/dnsmasq.conf.orig
echo 'interface=wlan1 # Listening interface
dhcp-range=192.168.4.1,192.168.4.20,255.255.255.0,24h
                # Pool of IP addresses served via DHCP
domain=wlan     # Local wireless DNS domain
address=/gw.wlan/192.168.4.1
                # Alias for this router' >> /etc/dnsmasq.conf

# restart services
sudo systemctl restart dhcpcd
sudo systemctl unmask hostapd
sudo systemctl enable hostapd
sudo systemctl start hostapd
sudo systemctl restart dnsmasq

# Bashrc --- Bashrc --- Bashrc --- Bashrc --- Bashrc --- Bashrc --- Bashrc --- Bashrc --- Bashrc ---
# bashrc aliases (for convenient)
echo 'alias ss-logs="sudo journalctl -u speakstick"
alias ss-server-logs="sudo journalctl -u speakstick-management-server"
alias ss-restart="sudo systemctl restart speakstick speakstick-management-server"

alias cdss="cd /opt/SpeakStick"
alias ss-update="git pull && ss-restart && echo "service restarted"' >> ~/.bashrc


# --- Audio --- Audio --- Audio --- Audio --- Audio --- Audio --- Audio --- Audio --- Audio --- Audio ---

# SDL_AUDIODRIVER=alsa
# SDL_AUDIODEV=/dev/audio




# Manual Steps --- Manual Steps --- Manual Steps --- Manual Steps --- Manual Steps --- Manual Steps ---

# change those lines in '/etc/nginx/sites-enabled/default':
# root /var/www/html; -> root /opt/SpeakStick/management-console/dist;
# server_name _; -> server_name speakstick.local;

# add `/index.html`` to the try_files in the default location `/`: 
# location / {
#   # First attempt to serve request as file, then
#   # as directory, then fall back to displaying a 404.
#   try_files $uri $uri/ /index.html =404;
# }

# add a new location to nginx config:
# location /api {
#   proxy_pass http://localhost:8080;
# }

# sudo nano /etc/default/hostapd
# replace: #DAEMON_CONF="" 
# with: DAEMON_CONF="/etc/hostapd/hostapd.conf"

# sudo nano /etc/init.d/hostapd
# replace: DAEMON_CONF= 
# with: DAEMON_CONF=/etc/hostapd/hostapd.conf






# usefull stuff:
# convert files to .wav
# https://cloudconvert.com/