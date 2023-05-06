python manage.py flush
python manage.py createsuperuser
python manage.py runscript ExtractUserData
python manage.py runscript CreateDummySurveys
rm -r ./media/EN/* ./media/FR/*