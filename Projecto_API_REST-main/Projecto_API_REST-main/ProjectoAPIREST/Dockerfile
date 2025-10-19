# Dockerfile para la API de películas
FROM python:3.9-slim

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema necesarias para PyMySQL y MySQL client
RUN apt-get update && apt-get install -y \
    pkg-config \
    default-libmysqlclient-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar archivos de dependencias
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY app.py .

# Exponer el puerto
EXPOSE 5000

# Comando para ejecutar la aplicación
CMD ["python", "app.py"]

