#celery -A app.celery_worker worker --loglevel=info
#python -c "import platform; print(platform.architecture())"
#celery -A app.celery_worker inspect registered