#! /bin/bash

# SpeakStick service
cp ./init/speakstick.service /usr/lib/systemd/system/speakstick.service
systemctl daemon-reload
systemctl enable speakstick

# SpeakStick management server service
cp ./init/speakstick-management-server.service /usr/lib/systemd/system/speakstick-management-server.service
systemctl daemon-reload
systemctl enable speakstick-management-server

# Network services
cp ./init/restart-network-services.service /usr/lib/systemd/system/restart-network-services.service
systemctl daemon-reload
systemctl enable restart-network-services

# logs handlers services
cp ./init/logs-handler.service /usr/lib/systemd/system/logs-handler.service
systemctl daemon-reload
systemctl enable logs-handler.service

cp ./init/logs-handler.timer /usr/lib/systemd/system/logs-handler.timer
systemctl daemon-reload
systemctl enable logs-handler.timer

# just to make sure everything is saved
systemctl daemon-reload