FROM python:3.8-slim-buster

WORKDIR /app
COPY . .
RUN pip3 install -r requirements.txt

CMD ["gunicorn", "app:app" ,"-b=0.0.0.0:8080","--timeout 99999999"]
