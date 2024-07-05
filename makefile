DC = docker compose
DEV = docker-compose-dev.yml

up-dev:
	${DC} -f ${DEV} up -d
down-dev:
	${DC} -f ${DEV} down