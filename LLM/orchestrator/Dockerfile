# Dockerfile para el microservicio de usuarios

FROM python:3.8-slim

WORKDIR /llorchestrator-service

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5016

CMD ["python", "llmorchestrator-service.py"]
