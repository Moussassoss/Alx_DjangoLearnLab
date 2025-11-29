from django.db import models

class Author(models.Model):
    """
    Author Model
    Stores information about an author.
    One Author can have multiple Books (one-to-many relationship).
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Book(models.Model):
    """
    Book Model
    Represents a book written by an Author.

    Fields:
    - title: title of the book
    - publication_year: year book was published
    - author: ForeignKey linking to Author (one-to-many)
    """
    title = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    author = models.ForeignKey(
        Author,
        related_name='books',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.title} ({self.publication_year})"
