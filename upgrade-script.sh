#! /bin/bash

latest_tag=$1

workdir="/opt/SpeakStick"
cd "${workdir}"

git fetch

if [ -z "$latest_tag" ]
then
    # check if automatic updates are enabled
    automatic_updates=$(sqlite3 ./configs.db "select value from configs where key='ENBALE_AUTOMATIC_UPDATES'")
    if [ $? = 0 ] && [ $automatic_updates = "0" ]
    then
        echo "Automatic updates are disabled, exiting"
        exit 0
    fi

    # get all tags and filter development build if needed
    development_builds=$(sqlite3 ./configs.db "select value from configs where key='ENABLE_DEVELOPMENT_BUILDS'")
    if [ $? != 0 ] || [ $development_builds != "1" ]
    then
        latest_tag=$(git tag -l --sort=-v:refname | grep -vE 'rc|dev' | head -n 1)
    else
        latest_tag=$(git tag -l --sort=-v:refname | head -n 1)
    fi
fi

current_version=$(git describe --tags)

echo "Upgrading from $current_version to $latest_tag"

git checkout $latest_tag

pip3 install -r requirements.txt

# Download console-management artifact
wget -P /tmp https://github.com/ofirl/SpeakStick/releases/download/$latest_tag/management-console.zip
# Decompress console-management artifact
rm -r /opt/SpeakStick/management-console/dist
unzip /tmp/management-console.zip -d /opt/SpeakStick/management-console
# Clean up
rm /tmp/management-console.zip

# Run migrations
/usr/bin/python3 -u /opt/SpeakStick/migrations/migrate.py ${current_version//v/} ${latest_tag//v/}

# update nginx.conf
sudo cp /opt/SpeakStick/init/nginx.conf /etc/nginx/sites-enabled/default
# reload nginx
sudo /etc/init.d/nginx reload

sudo ./init/init_systemctl_services.sh

# always restart the services last
sudo systemctl restart speakstick speakstick-management-server