## ----------------------------------------------------------------------
## Makefile is to manage Notifications project.
## ----------------------------------------------------------------------
compose_files=-f admin-docker-compose.yml -f kafka-docker-compose.yml -f rabbit-docker-compose.yml\
 -f redis-docker-compose.yml -f notices-docker-compose.yml -f elk-docker-compose.yml

help:     ## Show this help.
		@sed -ne '/@sed/!s/## //p' $(MAKEFILE_LIST)

start:  ## Start project infrastructure.
		cd docker && DOCKER_BUILDKIT=1 docker-compose $(compose_files) up -d --build --force-recreate
stop:  ## Stop infrastructure.
		cd docker && docker-compose $(compose_files) down

init:  ## First and full initialization. Create database, superuser and collect static files
	docker exec -it notice_django bash -c \
	'python manage.py migrate && python manage.py createsuperuser && python manage.py collectstatic --noinput'

migrate:  ## Apply migrations only
		docker exec -it notice_django bash -c 'python manage.py migrate'

restart: stop start
		