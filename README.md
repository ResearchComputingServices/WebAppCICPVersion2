# Run the server:

`python manage.py runserver`

# Create a super user:

`python manage.py createsuperuser`

# Update the DB:

`python manage.py makemigrations` *stages the updates for the database with new models/tables*

`python manage.py makemigrations <appname>` *To create initial migrations for an app, run makemigrations and specify the app name.*

`python manage.py migrate` *apply the staged updates*


