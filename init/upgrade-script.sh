#! /bin/bash

workdir="/opt/SpeakStick"

cd "${workdir}"
git pull
sudo systemctl restart speakstick speakstick-management-server

cd ../management-console

yarn deploy