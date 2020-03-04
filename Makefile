image:
	docker build . -t house-market-api

dev:
	pipenv run uvicorn api.entrypoint:api --reload
