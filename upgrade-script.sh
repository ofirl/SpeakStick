#! /bin/bash

workdir="/opt/SpeakStick"

cd "${workdir}"
git pull

cd management-console
yarn deploy

# always restart the services last
sudo systemctl restart speakstick speakstick-management-server