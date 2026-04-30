FROM python:3.11-slim

# Python çıktılarının terminale anında (bufferlanmadan) düşmesi için
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Gereksinimleri kopyala ve yükle
COPY requirements.txt /app/
# YENİ: --no-cache-dir eklendi
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Tüm proje dosyalarını kopyala
COPY . /app/
