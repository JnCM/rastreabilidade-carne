release: python manage.py migrate
web: gunicorn rastreio_carne_ufv.wsgi --timeout 120 --log-file=-
worker: celery -A site_app worker --loglevel=info --concurrency 10 -P solo
