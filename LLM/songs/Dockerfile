# Dockerfile para el microservicio de usuarios

FROM python:3.8-slim

WORKDIR /songs-service

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5012

CMD ["python", "songs-service.py"]
