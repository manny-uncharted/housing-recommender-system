#!/bin/bash

wget https://dl.google.com/linux/linux_signing_key.pub
sudo apt-key add linux_signing_key.pub
echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' | sudo tee -a /etc/apt/sources.list.d/google-chrome.list
sudo apt-get -y update
sudo apt-get install -y google-chrome-stable
sudo apt-get install -y qq unzip
wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip

unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

sudo apt install -y python3-selenium
pip install selenium==3.141.0 > /dev/null