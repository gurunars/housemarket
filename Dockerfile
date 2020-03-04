FROM python:alpine

RUN apk add --update-cache \
    python \
    python-dev \
    py-pip \
    build-base \
  && rm -rf /var/cache/apk/*

RUN pip install pipenv

EXPOSE 80

RUN mkdir /app

COPY ./Pipfile /app/
COPY ./Pipfile.lock /app/

WORKDIR /app

RUN pipenv install --system --deploy --ignore-pipfile

COPY ./api /app/api

CMD ["uvicorn", "api.entrypoint:api", "--host", "0.0.0.0", "--port", "80"]
