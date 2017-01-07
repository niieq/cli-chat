#!/bin/bash

VIRTUALENV_DIR=/home/vagrant/.virtualenvs/chat
PROJECT_DIR=cli-chat
VIRTUALENV_NAME=chat

echo "Installing pip"

curl -s https://bootstrap.pypa.io/get-pip.py | python3.4 > /dev/null 2>&1

echo "Mysql Setup"
apt-get install debconf-utils -y > /dev/null
debconf-set-selections <<< "mysql-server mysql-server/root_password password admin"
debconf-set-selections <<< "mysql-server mysql-server/root_password_again password admin"

apt-get install mysql-server -y > /dev/null

# Setting up MySQL user and db
mysql -uroot -padmin -e "CREATE DATABASE clichat" >> /vagrant/vm_build.log 2>&1

echo 'Installing and configuring virtualenvwrapper...'
pip install --quiet virtualenvwrapper==4.7.0

# setting up virtualenv & installing requirements 
su - vagrant -c "/usr/local/bin/virtualenv $VIRTUALENV_DIR --python=/usr/bin/python3.4 && \
    echo $PROJECT_DIR > $VIRTUALENV_DIR/.project && \
    $VIRTUALENV_DIR/bin/pip install -r $PROJECT_DIR/requirements.txt"

printf "export WORKON_HOME=/home/vagrant/.virtualenvs\n" >> /home/vagrant/.bashrc
printf "export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3.4\n" >> ~vagrant/.bashrc
printf "source /usr/local/bin/virtualenvwrapper.sh\n" >> ~vagrant/.bashrc
echo "workon $VIRTUALENV_NAME" >> /home/vagrant/.bashrc

su - vagrant -c "source $VIRTUALENV_DIR/bin/activate"