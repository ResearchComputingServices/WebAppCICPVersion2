#!/bin/bash

DJANGO_DIR=$(dirname $(realpath $0))


cd "$DJANGO_DIR"
source cicp_env/bin/activate

echo "Extracting User Data" >& /tmp/cronjob_lastrun.log
python3 manage.py runscript ExtractUserData 2>&1 >> /tmp/cronjob_lastrun.log
echo "Extracting Survey Data"  2>&1 >> /tmp/cronjob_lastrun.log
python3 manage.py runscript ExtractSurvey 2>&1 >> /tmp/cronjob_lastrun.log
