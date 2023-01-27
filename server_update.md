# Updating CICP code on Linux Server

These notes describe how to update an existing web app with the
latest code version from github.  For initial server installation, see
[these instructions](server_install.md).

## Become the root user

```bash
sudo -i
```

## Update source code

```bash
cd /webapp/WebAppCICPVersion2
git pull
```

## Sync Django to code changes

```bash
source cicp_env/bin/activate

# In case new code updates database models
python manage.py migrate

# In case new code adds additional static content (e.g. images, stylesheets)
python manage.py collectstatic

# In case new code requires additional python packages
pip install -r requirements.txt
```

## Restart web services

```bash
systemctl restart gunicorn
systemctl restart apache2
```

## Confirm service is running

```bash
# Are services running?  Some green text is good, some red text is bad!
systemctl status gunicorn
systemctl restart apache2
```

Also open website to make sure it still looks okay :-)
