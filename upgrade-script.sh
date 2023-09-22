#! /bin/bash

workdir="/opt/SpeakStick"
cd "${workdir}"

# check if automatic updates are enabled
automatic_updates=$(sqlite3 ./configs.db "select value from configs where key='ENBALE_AUTOMATIC_UPDATES'")
if [ $? = 0 ] && [ $automatic_updates = "0" ]
then
    echo "Automatic updates are disabled, exiting"
    exit 0
fi

latest_tag=$1
git fetch

if [ -z "$latest_tag" ]
then
    # get all tags
    latest_tag=$(git tag -l --sort=-v:refname)

    # filter development build if needed
    development_builds=$(sqlite3 ./configs.db "select value from configs where key='ENABLE_DEVELOPMENT_BUILDS'")
    if [ $? != 0 ] || [ $development_builds != "1" ]
    then
        latest_tag=$(echo $latest_tag | grep -vE 'rc|dev')
    fi

    # get the latest tag
    latest_tag=$(echo $latest_tag | head -n 1)
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