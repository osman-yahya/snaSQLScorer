# Tkinter desteği olan tam Python imajı
FROM python:3.9

# SQLite ve Tkinter bağımlılıkları
RUN apt-get update && apt-get install -y \
    sqlite3 \
    python3-tk \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama dosyalarını kopyala (isteğe bağlı)
COPY . .

# X11 forwarding için hazırlık (macOS)
ENV DISPLAY=host.docker.internal:0