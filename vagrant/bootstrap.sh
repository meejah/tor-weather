#!/usr/bin/env bash

# XXX FIXME this should be -- but is not -- "idempotent" (basically it
# just appends stuff to a few files, so they'll have an extra copy
# each run .. )

echo "Starting provisioning!"

# tell apt-get to work without a tty
export DEBIAN_FRONTEND=noninteractive

# update ubuntu package repo
echo "Updating repos..."
apt-get update > /dev/null
echo "Done!"
#apt-get upgrade -y

# install what we need for Weather proper
echo "Installing software-stack..."
# for python-requests >= 2.0, we install backports
cat >> /etc/apt/sources/list <<EOF
# Backports repository
deb http://ftp.debian.org/debian wheezy-backports main
EOF
apt-get update

apt-get install -y apache2 sqlite3 vim \
    libapache2-mod-wsgi \
    python-pip python-django python-requests

# onion_py from our internal source -- ultimately, should get OnionPy
# into Debian
# FIXME FIXME XXX
pushd /home/weather/opt/current/onion-py
pip install -e .
popd
echo "Done installing software stack!"

echo "Installing things for running tests"
apt-get install -y python-dev
pip install cyclone
echo "Done with testing installs"

# modify torrc
echo "Setting torrc accordingly..."
sudo -s
cat >> /etc/tor/torrc << EOF
FetchDirInfoEarly 1
FetchUselessDescriptors 1
ControlPort 9051
HashedControlPassword 16:067C5B9B7B036EEE603814A6F045B9EEE0B40EA60192506C005D64E436
EOF
echo "Done!"

echo "Reloading tor service..."
service tor reload
echo "Done!"

# prep weather-settings
echo "Prepping weather settings:"
echo "Create weather user"
useradd weather --groups debian-tor --create-home
echo "Create ~/opt/current"
mkdir -p ~weather/opt/current
echo "Done!"
fi

# generate ssl cert
echo "Generating SSL certificate..."
openssl req -new -newkey rsa:4096 \
    -x509 -days 365 -nodes -sha256 \
    -subj "/C=US/ST=Denial/L=Springfield/O=Dis/CN=weather.dev" \
    -out /etc/ssl/certs/weather.dev.pem \
    -keyout /etc/ssl/private/weather.dev.key
echo "Done!"

# configure apache
echo "Configuring apache..."
echo "Enable mod_rewrite..."
a2enmod rewrite
echo "Done"
echo "Enable mod_ssl..."
a2enmod ssl
echo "Done!"
echo "Set virtualhost..."
cat > /etc/apache2/sites-available/weather.dev << EOF
<VirtualHost *:80>
    ServerName weather.dev
    ErrorLog  /var/log/apache2/weather.dev-error.log
    CustomLog /var/log/apache2/weather.dev-access.log privacy
    WSGIScriptAlias / /home/weather/opt/current/weather/weather.wsgi
    RewriteEngine On
    RewriteRule ^(.*)$ https://%{SERVER_NAME}$1 [L,R]
</VirtualHost>
<VirtualHost *:443>
    SSLEngine on
    SSLCertificateFile    /etc/ssl/certs/weather.dev.pem
    SSLCertificateKeyFile /etc/ssl/private/weather.dev.key
    ServerName weather.dev
    AliasMatch ^/([^/]*\.png) /home/weather/opt/current/weather/media/$1
    AliasMatch ^/([^/]*\.css) /home/weather/opt/current/weather/media/$1
    AliasMatch ^/([^/]*\.js) /home/weather/opt/current/weather/media/$1
    Alias /media/ /home/weather/opt/current/weather/media/
    ErrorLog  /var/log/apache2/weather.dev-error.log
    CustomLog /var/log/apache2/weather.dev-access.log privacy
    WSGIScriptAlias / /home/weather/opt/current/weather/weather.wsgi
</VirtualHost>
EOF
echo "Done!"
echo "Enabling virtualhost..."
a2ensite weather.dev
a2dissite default
echo "Done!"

# sync weather
echo "Syncing weather-db..."
cd /home/weather/opt/current/weather && sudo -u www-data -H python manage.py syncdb --noinput
echo "ATTENTION: auto-creation of superuser 'vagrant' with pw 'vagrant'!!"
echo "Done!"

# run the commands that Sreenatha gave me, to "finish setting up the
# database". XXX FIXME do we really need to do this in this manner?
cd /home/weather/opt/current/weather
export DJANGO_SETTINGS_MODULE=settings
python manage.py clearmodels
#python manage.py rundaily
#python manage.py runhourly


echo "Restarting apache..."
service apache2 restart
echo "Done!"

echo "Done provisioning!"
