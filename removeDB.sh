rm db.sqlite3
rm -r InteractiveDB/migrations/__pycache__
rm InteractiveDB/migrations/0*

python3 manage.py makemigrations
python3 manage.py migrate

echo "Extracting User Data"
python3 manage.py runscript ExtractUserData

echo "Extracting Survey Data"
python3 manage.py runscript ExtractSurvey

python3 manage.py createsuperuser
