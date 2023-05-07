FROM python:3.10-slim-buster

WORKDIR	 /app

COPY . .

RUN pip install -r requirements.txt

EXPOSE 5000

CMD gunicorn --workers 1 --bind 0.0.0.0:5000 wsgi:app
