#!/usr/bin/env bash
 
echo "Starting provisioning!"

# update ubuntu package repo
echo "Updating repos..."
apt-get update > /dev/null
echo "Done!"
#apt-get upgrade -y

# install essentials
echo "Installing software-stack..."
apt-get install -y apache2 sqlite3 vim \
    libapache2-mod-wsgi tor \
    python-pip python-django
echo "Done installing software stack!"

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
echo "Create ~/opt/current"
echo "Set EMAIL_BACKEND"
echo "Set EMAIL_FILE_PATH"
useradd weather --groups debian-tor --create-home
mkdir ~weather/opt/current
grep EMAIL_BACKEND /home/weather/opt/current/weather/settings.py > /dev/null
if [ $? -ne 0 ]; then
    cat >> /home/weather/opt/current/weather/settings.py << EOF
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = '/tmp/weather-messages'
EOF
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
    WSGIScriptAlias / /home/weather/opt/current//weather/weather.wsgi
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
echo "Done!"
echo "Restarting apache..."
service apache2 restart
echo "Done!"

# sync weather
echo "Syncing weather-db..."
cd /home/weather/opt/current/weather && ./manage.py syncdb --noinput
echo "ATTENTION: auto-creation of superuser 'vagrant' with pw 'vagrant'!!"
echo "Done!"

echo "Done provisioning!"
