prod:
	docker-compose build
	docker-compose up

connect:
	docker-compose 

dev:
	pipenv run uvicorn api.entrypoint:api --reload
