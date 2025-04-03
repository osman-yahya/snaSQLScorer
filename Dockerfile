# Python 3.12 baz al (Tkinter desteği için 'slim' KULLANMA!)
FROM python:3.12

# requirements.txt'yi kopyala ve bağımlılıkları yükle
WORKDIR /env
COPY requirements.txt .
RUN apt-get update && apt-get install -y libsqlite3-dev
RUN pip install --no-cache-dir -r requirements.txt

# Kullanıcıya "ben ortamı hazırladım, sen lokal kodu çalıştır" mesajı
CMD echo "Python ortamı hazır! Şimdi şu komutu çalıştırın:" && \
    echo "python3 ./app/main.py"