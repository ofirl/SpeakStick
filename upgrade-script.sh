#! /bin/bash

workdir="/opt/SpeakStick"
cd "${workdir}"

latest_tag=$1
git fetch

if [ -z latest_tag ]
then
    latest_tag=$(git tag -l --sort=-v:refname | head -n 1)
fi

git checkout $latest_tag

pip3 install -r requirements.txt

cd management-console
yarn deploy

# always restart the services last
sudo systemctl restart speakstick speakstick-management-server