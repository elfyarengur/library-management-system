# library-management-system
Global AI Hub Python 202 Bootcamp Projesi - Kütüphane Yönetim Sistemi
Bu proje, **Global AI Hub Python 202 Bootcamp** için hazırlanmış bir **Kütüphane Yönetim Sistemi** uygulamasıdır.  
3 aşamadan oluşur:  
1. OOP ile terminal uygulaması  
2. Harici API (OpenLibrary) ile veri zenginleştirme  
3. FastAPI ile REST API  
---
## Kurulum
```bash
git clone <repo-link>
cd <repo-adi>
pip install -r requirements.txt
```
---
## Terminal Uygulaması
```bash
python main.py terminal
```
 Menü:  
1. Kitap Ekle (ISBN – API)  
2. Kitap Ekle (Manuel)  
3. Kitap Sil  
4. Kitapları Listele  
5. Kitap Ara  
6. Çıkış  
---
## API Sunucusu
```bash
python main.py api
```
 Çalıştırdıktan sonra tarayıcıdan şu adrese gidin:  
 [http://localhost:8000/docs](http://localhost:8000/docs)  

### API Endpoint’leri
- **GET /books** → Kayıtlı kitapları listeler  
- **POST /books** → ISBN alır ve API’den kitabı ekler  
  ```json
  {
    "isbn": "9780439708180"
  }
  ```
- **DELETE /books/{isbn}** → ISBN ile kitabı siler  
---
## Testler
```bash
pytest -v
```
---
## Notlar
- Veriler `library.json` dosyasında saklanır.  
- API üzerinden eklenen kitaplar `api_library.json` içinde tutulur.  
- İleri seviye: SQLite veya Docker entegrasyonu eklenebilir.

