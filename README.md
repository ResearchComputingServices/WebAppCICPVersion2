# Run the server:

`python manage.py runserver`

# Create a super user:

`python manage.py createsuperuser`

# Update the DB:

`python manage.py makemigrations` *stages the updates for the database with new models/tables*

`python manage.py makemigrations <appname>` *To create initial migrations for an app, run makemigrations and specify the app name.*

`python manage.py migrate` *apply the staged updates*


# Remove the DB:

During development if you need to start the DB over from scratch do the following:

rm db.sqlite3
remove everything in  InteractiveDB/migrations/ except __init__.py

then rebuild the DB:

`python manage.py makemigrations <appname>`

`python manage.py migrate`
