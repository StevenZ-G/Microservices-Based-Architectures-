# Dockerfile para el microservicio de usuarios

FROM python:3.8-slim

WORKDIR /emotions-songs-service

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5013

CMD ["python", "emotions-songs-service.py"]
