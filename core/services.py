from models import Book


def create_book(title: str, author: str) -> Book:
    return Book.objects.create(title=title, author=author)
