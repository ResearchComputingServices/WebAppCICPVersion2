#!/bin/bash

DJANGO_DIR=$(dirname $(realpath $0))


cd "$DJANGO_DIR"
source cicp_env/bin/activate

python3 manage.py runscript cronJobScript >& /tmp/cronjob_lastrun.log
