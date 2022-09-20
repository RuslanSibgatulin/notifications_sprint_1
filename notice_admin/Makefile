## ----------------------------------------------------------------------
## Makefile is to manage Notice Admin.
## ----------------------------------------------------------------------
include .env
export

help:     ## Show this help.
		@sed -ne '/@sed/!s/## //p' $(MAKEFILE_LIST)

start:  ## Start project
		python app/manage.py runserver
migrate:  ## Apply databsea changes
		python app/manage.py makemigrations
		python app/manage.py migrate
