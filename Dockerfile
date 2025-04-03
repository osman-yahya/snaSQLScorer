# Temel Python imajı
FROM python:3.12

# Çalışma dizinini ayarla
WORKDIR /app

# Bağımlılıkları kopyala ve yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Tüm proje dosyalarını kopyala
COPY . .

# Veritabanı dosyasının yazılabilir olması için izinleri ayarla
RUN chmod a+w /app/database.db

# Uygulamayı çalıştır
CMD ["python", "./app/main.py"]