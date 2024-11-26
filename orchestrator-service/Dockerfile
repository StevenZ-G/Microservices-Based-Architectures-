# Utilizar la imagen base de Python
FROM python:3.8-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar solo el archivo requirements.txt para aprovechar el cache
COPY requirements.txt /app/

# Actualizar pip e instalar las dependencias
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copiar el contenido del directorio local al contenedor
COPY . /app

# Exponer el puerto 5004 para Flask
EXPOSE 5004

# Comando para iniciar la aplicación Flask
CMD ["python", "app.py"]
