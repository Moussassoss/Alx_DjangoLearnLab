from bookshelf.models import Book
books = Book.objects.get()
for b in books:
    print(b.title, b.author, b.publication_year)
# Expected Output: 1984 George Orwell 1949
