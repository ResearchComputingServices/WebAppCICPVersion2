# Installing CICP Weekly Report on Linux Server

**Note: Many of these commands run as root.  Either use sudo for those commands, or use `sudo -i` to switch to root user**

## Install Prerequisite Software

First run:
```bash
sudo apt udpate
```
Run these commands to install Ubuntu software packages:

```bash
apt install python-is-python3
apt install python3-virtualenv
apt install apache2
apt install mysql-server
apt install libmysqlclient-dev
```

## Configure Database

Replace MYSQL_PASSWORD and MYSQL_ROOT_PASSWORD with secret passwords in the following shell commands:

```bash
mysql -e 'create database cicp_reports'
mysql -e 'CREATE USER cicp@localhost IDENTIFIED BY "MYSQL_PASSWORD";'
mysql -e 'GRANT ALL ON cicp_reports.* TO cicp@localhost;'
mysql -e 'ALTER USER root@localhost IDENTIFIED WITH mysql_native_password BY "MYSQL_ROOT_PASSWORD";'
mysql_secure_installation
```


## Install Python Web App

Run these shell commands to download the Python code and create a
virtual environment:

```bash
mkdir /webapp
adduser  --system --home /nonexistent --no-create-home --disabled-login --shell /usr/sbin/nologin django
cd /webapp

git clone https://github.com/ResearchComputingServices/WebAppCICPVersion2.git
cd WebAppCICPVersion2


# Create folders for static web assets
mkdir /var/www/html/static
mkdir /var/www/html/media

# Allow gunicorn to write to data folders
## DISABLED: The cronjob runs as root, and I think the django app running from gunicorn
##           only needs read-only to these directories
#chown -R django Data
#chown -R django /var/www/html/media

virtualenv cicp_env
source cicp_env/bin/activate
pip install -r requirements.txt
# These *might* not already be in requirements.txt:
pip install mysqlclient mycli gunicorn
python -c 'import nltk; nltk.download("punkt")'
python -c "import nltk; nltk.download('stopwords')"
```

To start the Python web service automatically, we use Ubuntu's systemd
to control the gunicorn python service.  Create the file
`/etc/systemd/system/gunicorn.service` with these contents:

```conf
[Unit]
Description=gunicorn service
After=network.target
   
[Service]
User=django
Group=nogroup
WorkingDirectory=/webapp/WebAppCICPVersion2
ExecStart=/webapp/WebAppCICPVersion2/cicp_env/bin/gunicorn --access-logfile - --workers 8 --timeout 300 --bind 127.0.0.1:8000 WebAppCICPVersion2.wsgi:application
   
[Install]
WantedBy=multi-user.target
```

## Configure Python Web App

Copy settings.py and change the following

  1. Set `DEBUG = False`
  2. Set `ALLOWED_HOSTS = ['*']`   **TODO: RESTRICT THIS FOR SECURITY?**
  3. Set `SECRET_KEY` to something secret
  4. Set `STATIC_ROOT` to `'/var/www/html/static/'`
  4. Set `MEDIA_ROOT` to `'/var/www/html/media/'`
  4. In the `DATABASES` section replace sqlite3 with mysql settings.
     MYSQL_PASSWORD should match the password you already created
```conf
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'cicp_reports',
        'USER': 'cicp',
        'PASSWORD': 'MYSQL_PASSWORD',
        'HOST': 'localhost',
        'PORT': '3306',
    }
````


Then finish setting up the django app

```bash
source cicp_env/bin/activate
python ./manage.py migrate
python ./manage.py collectstatic
```

And then we need to start gunicorn server, and enable it to start on boot:
```bash
systemctl daemon-reload
systemctl enable gunicorn
systemctl start gunicorn
```

## Configure Apache Webserver

Enable proxying to gunicorn, enable SSL (https), and disable some unecessary stuff:

```bash
a2enmod proxy_http
a2enmod ssl
a2enmod rewrite
a2dismod status
a2disconf serve-cgi-bin
a2ensite default-ssl.conf
```

Setup an SSL certificate.  In this example I'm using a self-signed
certificate, but you could go also look into getting a properly signed
cert:

```bash
# For now I'm using a self signed certificate
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/private/apache-selfsigned.key -out /etc/ssl/certs/apache-selfsigned.crt
```

Edit the file `/etc/apache2/sites-enabled/000-default.conf` and make these changes:
```conf
    RewriteEngine On
    RewriteRule ^(.*)$ https://%{HTTP_HOST}$1 [R=301,L]
```

Edit the file `/etc/apache2/sites-available/default-ssl.conf` and make these changes:
```conf
   SSLCertificateFile	/etc/ssl/certs/apache-selfsigned.crt
   SSLCertificateKeyFile /etc/ssl/private/apache-selfsigned.key
   
   # Special log formatting/filtering because we are behind F5 reverse proxy
   LogFormat "%{X-Forwarded-For}i %h %l %u [%L] %t \"%r\" %>s %O \"%{Referer}i\" \"%{User-Agent}i\"" f5combined
   SetEnvIf Remote_Addr "10\.254\.159\.[34]" isF5
   ErrorLog ${APACHE_LOG_DIR}/error.log
   CustomLog ${APACHE_LOG_DIR}/access.log f5combined env=!isF5
   
   <Location "/admin">
       SetEnvIf X-Forwarded-For "^134\.117\." internal_ip
       Require env internal_ip
   </Location>

   ProxyPass /static/ !
   ProxyPass /media/  !
   ProxyPass / http://localhost:8000/
   ProxyPassReverse / http://localhost:8000/
```

Edit the file `/etc/apache2/apache2.conf` and disable the Indexes and FollowSymLinks options:
```conf
<Directory />
        Options -FollowSymLinks
        AllowOverride None
        Require all denied
</Directory>

# <Directory /usr/share>
#       AllowOverride None
#       Require all granted
# </Directory>

<Directory /var/www/>
        Options -Indexes -FollowSymLinks
        AllowOverride None
        Require all granted
</Directory>
```



Edit the file `/etc/apache2/conf-enabled/security.conf` and make these changes:
```conf
ServerTokens Prod
ServerSignature Off
```

Then restart the Apache webserver to load the config changes:
```bash
systemctl restart apache2
```

## Setup Cronjob

Make sure the cronjob.sh script is executable and then edit the cronjobs:

```bash
chmod +x cronjob.sh
crontab -e
```

In the crontab file, add line like the following.
In this example, we set the cronjob to run at 3:00AM on every Thursday.
Edit the crontab using the command `crontab -e`
```conf
00 03    *  *  4    /webapp/WebAppCICPVersion2/cronjob.sh
```
