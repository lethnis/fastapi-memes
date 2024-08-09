DC = docker compose
DEV = docker-compose-dev.yml

dev-up:
	${DC} -f ${DEV} up -d
dev-down:
	${DC} -f ${DEV} down