# SQLScorer Kurulum ve Kullanım Kılavuzu

SQLScorer, Python tabanlı bir uygulama olup dosya seçme işlemleri için GUI kullanır ve bu nedenle Docker ile dağıtılamaz. Docker, dahili bir GUI'ye sahip olmadığı için, bu kurulum için aşağıdaki yönergeleri takip etmeniz gerekmektedir.

## Sistem Gereksinimleri

- Python 3.x
- Git

### macOS Kurulumu

Sırasıyla aşağıdaki komutları bilgisayarınızda çalıştırın :
`git clone https://github.com/osman-yahya/snaSQLScorer`

`cd snaSQLScorer`

`python3 -m venv gvenv`

`source gvenv/bin/activate`

`pip install --no-cache-dir -r requirements.txt`

`python3 ./app/main.py`

### Windows Kurulumu

Sırasıyla aşağıdaki komutları bilgisayarınızda çalıştırın :
`git clone https://github.com/osman-yahya/snaSQLScorer`

`cd snaSQLScorer`

`python -m venv gvenv`

`gvenv/Scripts/Activate`

`pip install --no-cache-dir -r requirements.txt`

`python ./app/main.py`

## Veritabanı Yapısı

Eğer özel SQL sorguları oluşturmak isterseniz, aşağıdaki gibi bir veritabanı yapısına sahip olacaksınız:

### `database.db` İçerisindeki Tablolar

#### 1. `workers` Tablosu
- `id`: Çalışan ID
- `isim`: Çalışan adı
- `soyisim`: Çalışan soyadı
- `email`: Çalışan e-posta adresi
- `isManager`: Çalışanın yönetici olup olmadığı (boolean)
- `maas`: Çalışanın maaşı

**Veri Örneği:**
- 16 yönetici (`id` ile 1'e sahip), toplamda 152 dummy kullanıcı.

#### 2. `companies` Tablosu
- `id`: Şirket ID
- `sirketIsim`: Şirket adı

**Veri Örneği:**
- Toplamda 10 dummy şirket.

#### 3. `workload` Tablosu
- `id`: Çalışma ID
- `worker_id`: Çalışan ID (foreign key)
- `company_id`: Şirket ID (foreign key)
- `hours_worked`: Çalışan tarafından çalışılan saat sayısı
- `date`: Çalışma tarihi