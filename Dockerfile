FROM python:3.12

WORKDIR /app
COPY requirements.txt .

# Virtual environment'i PROJE DİZİNİNE kur
RUN python -m venv ./venv && \
    ./venv/bin/pip install --no-cache-dir -r requirements.txt

# Sadece bilgilendirme mesajı
CMD echo "Virtual environment hazır! Çalıştırmak için:" && \
    echo "source venv/bin/activate && python app/main.py"