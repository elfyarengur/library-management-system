"""
Global AI Hub Python 202 Bootcamp Projesi
Kütüphane Yönetim Sistemi
"""

import json
import httpx
import sys
from typing import List, Optional

# ===== AŞAMA 1: OOP İLE TERMİNAL UYGULAMASI =====

class Book:
    """Kitap sınıfı - Her bir kitabı temsil eder"""
    def __init__(self, title: str, author: str, isbn: str):
        self.title = title
        self.author = author
        self.isbn = isbn
    
    def __str__(self):
        return f"{self.title} by {self.author} (ISBN: {self.isbn})"
    
    def to_dict(self):
        """Kitap bilgilerini sözlük formatında döndürür"""
        return {
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Sözlükten Book nesnesi oluşturur"""
        return cls(data["title"], data["author"], data["isbn"])


class Library:
    """Kütüphane sınıfı - Tüm operasyonları yönetir"""
    def __init__(self, filename: str = "library.json"):
        self.filename = filename
        self.books = []
        self.load_books()
    
    def add_book(self, book: Book) -> Book:
        """Yeni kitap ekler"""
        self.books.append(book)
        self.save_books()
        return book
    
    def add_book_by_isbn(self, isbn: str) -> Optional[Book]:
        """ISBN ile API'den kitap bilgilerini çeker ve ekler"""
        try:
            # Open Library API'sine istek gönder
            url = f"https://openlibrary.org/isbn/{isbn}.json"
            response = httpx.get(url, timeout=10.0)
            
            if response.status_code == 200:
                book_data = response.json()
                
                # Kitap başlığını al
                title = book_data.get("title", "Bilinmeyen Başlık")
                
                # Yazar bilgisini al
                author_name = "Bilinmeyen Yazar"
                authors = book_data.get("authors", [])
                
                if authors:
                    # Basit yöntemle yazar ismini al
                    if isinstance(authors[0], dict):
                        author_name = authors[0].get("name", "Bilinmeyen Yazar")
                    else:
                        author_name = str(authors[0])
                
                # Yeni kitap oluştur ve ekle
                book = Book(title, author_name, isbn)
                return self.add_book(book)
            else:
                print(f"❌ Kitap bulunamadı. HTTP Status: {response.status_code}")
                return None
                
        except httpx.RequestError as e:
            print(f"❌ API bağlantı hatası: {e}")
            return None
        except Exception as e:
            print(f"❌ Beklenmeyen hata: {e}")
            return None
    
    def remove_book(self, isbn: str) -> bool:
        """ISBN ile kitap siler"""
        initial_count = len(self.books)
        self.books = [book for book in self.books if book.isbn != isbn]
        if len(self.books) < initial_count:
            self.save_books()
            return True
        return False
    
    def list_books(self) -> List[Book]:
        """Tüm kitapları listeler"""
        return self.books
    
    def find_book(self, isbn: str) -> Optional[Book]:
        """ISBN ile kitap bulur"""
        for book in self.books:
            if book.isbn == isbn:
                return book
        return None
    
    def load_books(self):
        """Kitapları JSON dosyasından yükler"""
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                data = json.load(file)
                self.books = [Book.from_dict(book_data) for book_data in data]
                print(f"✅ {len(self.books)} kitap yüklendi.")
        except FileNotFoundError:
            print("ℹ️  Dosya bulunamadı, yeni kütüphane oluşturuluyor.")
            self.books = []
        except json.JSONDecodeError:
            print("ℹ️  JSON decode hatası, yeni kütüphane oluşturuluyor.")
            self.books = []
        except Exception as e:
            print(f"❌ Kitaplar yüklenirken hata: {e}")
            self.books = []
    
    def save_books(self):
        """Kitapları JSON dosyasına kaydeder"""
        try:
            with open(self.filename, 'w', encoding='utf-8') as file:
                json_data = [book.to_dict() for book in self.books]
                json.dump(json_data, file, indent=4, ensure_ascii=False)
            print(f"💾 {len(self.books)} kitap kaydedildi.")
        except Exception as e:
            print(f"❌ Kitaplar kaydedilirken hata: {e}")


def run_terminal_app():
    """Terminal uygulamasını çalıştırır"""
    library = Library()
    
    while True:
        print("\n" + "="*50)
        print("📚 KÜTÜPHANE YÖNETİM SİSTEMİ")
        print("="*50)
        print("1. 📖 Kitap Ekle (ISBN ile - API)")
        print("2. 📝 Kitap Ekle (Manuel)")
        print("3. 🗑️  Kitap Sil")
        print("4. 📋 Kitapları Listele")
        print("5. 🔍 Kitap Ara")
        print("6. 🚪 Çıkış")
        print("="*50)
        
        choice = input("👉 Seçiminiz (1-6): ").strip()
        
        if choice == "1":
            isbn = input("📘 ISBN: ").strip()
            if not isbn:
                print("❌ ISBN boş olamaz!")
                continue
                
            book = library.add_book_by_isbn(isbn)
            if book:
                print(f"✅ Kitap başarıyla eklendi: {book}")
            else:
                print("❌ Kitap bulunamadı veya API hatası oluştu.")
        
        elif choice == "2":
            title = input("📘 Kitap Adı: ").strip()
            author = input("👤 Yazar: ").strip()
            isbn = input("🔢 ISBN: ").strip()
            
            if not title or not author or not isbn:
                print("❌ Tüm alanlar doldurulmalıdır!")
                continue
                
            book = Book(title, author, isbn)
            library.add_book(book)
            print("✅ Kitap başarıyla eklendi!")
        
        elif choice == "3":
            isbn = input("🗑️  Silmek istediğiniz kitabın ISBN'si: ").strip()
            if library.remove_book(isbn):
                print("✅ Kitap başarıyla silindi!")
            else:
                print("❌ Bu ISBN'e sahip kitap bulunamadı.")
        
        elif choice == "4":
            books = library.list_books()
            if not books:
                print("📭 Kütüphanede kitap bulunmamaktadır.")
            else:
                print(f"\n📚 Kütüphanedeki Kitaplar ({len(books)} adet):")
                print("-" * 70)
                for i, book in enumerate(books, 1):
                    print(f"{i:2d}. {book}")
        
        elif choice == "5":
            isbn = input("🔍 Aramak istediğiniz kitabın ISBN'si: ").strip()
            book = library.find_book(isbn)
            if book:
                print(f"✅ Kitap bulundu: {book}")
            else:
                print("❌ Kitap bulunamadı.")
        
        elif choice == "6":
            print("👋 Çıkış yapılıyor...")
            break
        
        else:
            print("❌ Geçersiz seçim. Lütfen 1-6 arasında bir sayı girin.")


# ===== AŞAMA 3: FASTAPI İLE WEB SERVİSİ =====

try:
    from fastapi import FastAPI, HTTPException, status
    from pydantic import BaseModel
    import uvicorn
    
    # FastAPI uygulaması
    app = FastAPI(
        title="Kütüphane Yönetim API",
        description="Kitap ekleme, silme ve listeleme işlemleri için REST API",
        version="1.0.0"
    )

    # Global kütüphane nesnesi
    library_api = Library("api_library.json")

    # Pydantic modelleri
    class ISBNRequest(BaseModel):
        isbn: str

        class Config:
            json_schema_extra = {
                "example": {
                    "isbn": "9780439708180"
                }
            }

    class BookResponse(BaseModel):
        title: str
        author: str
        isbn: str
        
        @classmethod
        def from_book(cls, book: Book):
            return cls(title=book.title, author=book.author, isbn=book.isbn)

    # API endpoint'leri
    @app.get("/", include_in_schema=False)
    async def root():
        return {"message": "Kütüphane Yönetim API'sine hoş geldiniz! Dökümantasyon için /docs adresini ziyaret edin."}

    @app.get("/books", 
             response_model=List[BookResponse],
             summary="Tüm kitapları listeler",
             description="Kütüphanede kayıtlı tüm kitapların listesini döndürür.")
    async def get_books():
        books = library_api.list_books()
        return [BookResponse.from_book(book) for book in books]

    @app.post("/books", 
              response_model=BookResponse,
              status_code=status.HTTP_201_CREATED,
              summary="ISBN ile kitap ekler",
              description="Open Library API'sini kullanarak ISBN numarası ile kitap bilgilerini çeker ve kütüphaneye ekler.")
    async def add_book(isbn_request: ISBNRequest):
        book = library_api.add_book_by_isbn(isbn_request.isbn)
        if book:
            return BookResponse.from_book(book)
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Belirtilen ISBN ile kitap bulunamadı veya API erişiminde sorun oluştu."
            )

    @app.delete("/books/{isbn}",
                summary="ISBN ile kitap siler",
                description="Belirtilen ISBN numarasına sahip kitabı kütüphaneden siler.")
    async def delete_book(isbn: str):
        if library_api.remove_book(isbn):
            return {"message": "Kitap başarıyla silindi"}
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Belirtilen ISBN ile kitap bulunamadı"
            )

    def run_api_server():
        """API sunucusunu çalıştırır"""
        print("🌐 API sunucusu başlatılıyor...")
        print("📚 Dokümantasyon: http://localhost:8000/docs")
        print("⏹️  Durdurmak için Ctrl+C")
        uvicorn.run(app, host="0.0.0.0", port=8000)

except ImportError:
    def run_api_server():
        print("❌ FastAPI veya uvicorn yüklü değil!")
        print("💡 Yüklemek için: python -m pip install --user fastapi uvicorn")


# ===== ANA PROGRAM =====

if __name__ == "__main__":
    print("📚 Global AI Hub Python 202 Bootcamp Projesi")
    print("🔧 Kütüphane Yönetim Sistemi - httpx ile")
    print("="*50)
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "terminal":
            run_terminal_app()
        elif command == "api":
            run_api_server()
        else:
            print("❌ Geçersiz komut.")
    else:
        # İnteraktif menü
        while True:
            print("\n🔍 Ne yapmak istersiniz?")
            print("1. 🖥️  Terminal Uygulamasını Başlat")
            print("2. 🌐 API Sunucusunu Başlat")
            print("3. 🚪 Çıkış")
            
            choice = input("👉 Seçiminiz (1-3): ").strip()
            
            if choice == "1":
                run_terminal_app()
                break
            elif choice == "2":
                run_api_server()
                break
            elif choice == "3":
                print("👋 Görüşmek üzere!")
                break
            else:
                print("❌ Geçersiz seçim!")