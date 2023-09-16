#! /bin/bash

sleep 10
sudo systemctl restart hostapd dhcpcd dnsmasq

sleep 10
sudo systemctl restart hostapd dhcpcd dnsmasq