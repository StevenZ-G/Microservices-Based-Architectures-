# Usa la imagen base de Python
FROM python:3.8-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar el código fuente y las dependencias al contenedor
COPY app.py /app/app.py
COPY requirements.txt /app/requirements.txt

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto 5004 para el orquestador
EXPOSE 5004

# Comando para ejecutar la aplicación
CMD ["python", "app.py"]
