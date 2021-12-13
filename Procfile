release: python manage.py migrate
web: gunicorn rastreio_carne_ufv.wsgi --log-file=-
worker: celery -A site_app worker --loglevel=info --concurrency 1 -P solo
