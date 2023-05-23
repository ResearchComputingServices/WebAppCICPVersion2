python manage.py flush
python manage.py createsuperuser
python manage.py runscript ExtractUserData
python manage.py runscript CreateDummySurveys
rm -r /var/www/html/media/DefaultImages/EN/* /var/www/html/media/DefaultImages/FR/*