release: bash ./Procfile_release.sh
web: gunicorn simpellab.wsgi
worker: python ./manage.py rqworker high default low