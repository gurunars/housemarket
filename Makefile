prod:
	docker-compose build
	docker-compose up

dev:
	pipenv run uvicorn api.entrypoint:api --reload
