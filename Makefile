prepare_env:
	touch env/.envtest && echo \
"\
# ===== BASE SETTINGS =====\n\
DJANGO_LOG_LEVEL=INFO\n\
DJANGO_DEBUG=True\n\
DJANGO_SECRET_KEY=13212eeddcvadsfsadfsdacadf\n\
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost\n\n\
# ===== DATABASE SETTINGS =====\n\
DATABASE_ENGINE=django.db.backends.postgresql_psycopg2\n\
DATABASE_HOST=postgres\n\
DATABASE_PORT=5432\n\
DATABASE_NAME=ref_db\n\
DATABASE_USER=postgres\n\
DATABASE_PASSWORD=postgres\n\n\
# ===== REDIS SETTINGS =====\n\
REDIS_HOST=redis\n\
REDIS_PORT=6379\
" > env/.envtest

	touch env/.envtest2 && echo \
   "\
POSTGRES_DB=store_db\n\
POSTGRES_USER=store_username\n\
POSTGRES_PASSWORD=store_password\
" > env/.envtest2

docker_run:
	docker-compose -f docker-compose.yaml up -d --build

docker_stop:
	docker-compose -f docker-compose.yaml down -v

poetry_setup:
	poetry config virtualenvs.in-project true
	poetry shell
	poetry install

django_run:
	cd app
	python manage.py makemigrations
	python manage.py migrate
	python manage.py runserver

redis_run:
	redis-server

celery_run:
	celery -A config worker --loglevel=INFO

test:
	pytest

test_linters:
	pre-commit install
	pre-commit run --all-files
