## ----------------------------------------------------------------------
## The purpose of this Makefile is to manage Notifications project.
## ----------------------------------------------------------------------
compose_files=-f kafka-docker-compose.yml -f elk-docker-compose.yml -f rabbit-docker-compose.yml

help:     ## Show this help.
		@sed -ne '/@sed/!s/## //p' $(MAKEFILE_LIST)

start:  ## Start project infrastructure.
		cd docker && DOCKER_BUILDKIT=1 docker-compose $(compose_files) up -d --build --force-recreate
stop:  ## Stop infrastructure.
		cd docker && docker-compose $(compose_files) down
