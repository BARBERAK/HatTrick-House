# Usamos una versión ligera de Python
FROM python:3.14-slim

# Evitamos que Python cree archivos basura y fuerzamos a mostrar los logs en la terminal
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Creamos la carpeta de trabajo dentro del contenedor
WORKDIR /app

# Copiamos todo el código al contenedor
COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/