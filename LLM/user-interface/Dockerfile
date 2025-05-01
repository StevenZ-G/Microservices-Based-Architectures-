# Dockerfile para el microservicio de usuarios

FROM python:3.8-slim

WORKDIR /user-service

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5010

CMD ["python", "user-service.py"]
