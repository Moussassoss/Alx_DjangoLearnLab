from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from .models import Book, Author


class BookAPITestCase(APITestCase):

    def setUp(self):
        # Test user
        self.user = User.objects.create_user(username="moussa", password="password123")

        # Create an author
        self.author = Author.objects.create(name="John Doe")

        # Create some books
        self.book1 = Book.objects.create(
            title="Python Basics",
            publication_year=2020,
            author=self.author
        )

        self.book2 = Book.objects.create(
            title="Django Advanced",
            publication_year=2021,
            author=self.author
        )

        self.client = APIClient()

    # --------------------------------------------------
    # TEST LIST VIEW
    # --------------------------------------------------
    def test_list_books(self):
        url = reverse("book-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    # --------------------------------------------------
    # TEST DETAIL VIEW
    # --------------------------------------------------
    def test_retrieve_single_book(self):
        url = reverse("book-detail", args=[self.book1.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Python Basics")

    # --------------------------------------------------
    # TEST CREATE VIEW (AUTH REQUIRED)
    # --------------------------------------------------
    def test_create_book_requires_authentication(self):
        url = reverse("book-create")
        data = {
            "title": "New Book",
            "publication_year": 2022,
            "author": self.author.id
        }

        # Without auth
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # With auth
        self.client.login(username="moussa", password="password123")
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)

    # --------------------------------------------------
    # TEST UPDATE VIEW (AUTH REQUIRED)
    # --------------------------------------------------
    def test_update_book(self):
        url = reverse("book-update", args=[self.book1.id])
        data = {"title": "Updated Title", "publication_year": 2020, "author": self.author.id}

        # Without auth
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # With auth
        self.client.login(username="moussa", password="password123")
        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Updated Title")

    # --------------------------------------------------
    # TEST DELETE VIEW (AUTH REQUIRED)
    # --------------------------------------------------
    def test_delete_book(self):
        url = reverse("book-delete", args=[self.book1.id])

        # Without auth
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # With auth
        self.client.login(username="moussa", password="password123")
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)

    # --------------------------------------------------
    # TEST FILTERING
    # --------------------------------------------------
    def test_filter_books_by_title(self):
        url = reverse("book-list") + "?title=Python Basics"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    # --------------------------------------------------
    # TEST SEARCH
    # --------------------------------------------------
    def test_search_books(self):
        url = reverse("book-list") + "?search=django"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Django Advanced")

    # --------------------------------------------------
    # TEST ORDERING
    # --------------------------------------------------
    def test_order_books_by_year(self):
        url = reverse("book-list") + "?ordering=publication_year"
        response = self.client.get(url)

        years = [book["publication_year"] for book in response.data]
        self.assertEqual(years, sorted(years))
