#! /bin/bash

workdir="/opt/SpeakStick"
cd "${workdir}"

latest_tag=$1
git fetch

if [ -z "$latest_tag" ]
then
    latest_tag=$(git tag -l --sort=-v:refname | head -n 1)
fi

echo "Upgrading to $latest_tag"

git checkout $latest_tag

pip3 install -r requirements.txt

# Download console-management artifact
wget -P /tmp https://github.com/ofirl/SpeakStick/releases/download/$latest_tag/management-console.zip
# Decompress console-management artifact
rm -r /opt/SpeakStick/management-console/dist
unzip /tmp/management-console.zip -d /opt/SpeakStick/management-console
# Clean up
rm /tmp/management-console.zip

# always restart the services last
sudo systemctl restart speakstick speakstick-management-server