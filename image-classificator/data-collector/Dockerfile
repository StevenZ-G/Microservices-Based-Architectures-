# Utilizar la imagen base de Python
FROM python:3.8-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar el contenido del directorio local al contenedor
COPY . /app

# Instalar las dependencias necesarias
RUN pip install -r requirements.txt

# Exponer el puerto 5000 para Flask
EXPOSE 5000

# Comando para iniciar la aplicación Flask
CMD ["python", "app.py"]
