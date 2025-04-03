FROM python:3.12

WORKDIR /app
COPY requirements.txt .

# Virtual environment oluştur ve bağımlılıkları yükle
RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

# Kullanıcıya virtual environment'i aktaracak komut
CMD ["bash", "-c", "cp -r /opt/venv /app/venv && echo 'Virtual environment /app/venv oluşturuldu. Lokalde çalıştırmak için: source venv/bin/activate && python app/main.py'"]