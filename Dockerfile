FROM python:3.9.6-bullseye

COPY . /app
COPY ./entrypoint.sh /app/entrypoint.sh
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r ./requirements.txt

ENTRYPOINT ["sh", "entrypoint.sh"]
