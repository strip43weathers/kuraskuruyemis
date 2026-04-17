FROM python:3.11-slim

# Python çıktılarının terminale anında (bufferlanmadan) düşmesi için
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Gereksinimleri kopyala ve yükle
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Tüm proje dosyalarını kopyala
COPY . /app/
