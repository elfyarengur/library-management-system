import pytest
from main import Book, Library

@pytest.fixture
def library(tmp_path):
    """Geçici JSON dosyasıyla test için kütüphane"""
    file_path = tmp_path / "test_library.json"
    return Library(filename=str(file_path))

def test_add_and_find_book(library):
    book = Book("Test Kitabı", "Test Yazar", "123456")
    library.add_book(book)
    found = library.find_book("123456")
    assert found is not None
    assert found.title == "Test Kitabı"

def test_remove_book(library):
    book = Book("Silinecek", "Yazar", "654321")
    library.add_book(book)
    assert library.remove_book("654321") is True
    assert library.find_book("654321") is None

def test_list_books(library):
    library.add_book(Book("Kitap1", "Yazar1", "111"))
    library.add_book(Book("Kitap2", "Yazar2", "222"))
    books = library.list_books()
    assert len(books) == 2
    assert books[0].title == "Kitap1"
    assert books[1].title == "Kitap2"
