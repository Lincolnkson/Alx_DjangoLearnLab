from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Book, Author
from .serializers import BookSerializer
import json

class BookAPITestCase(TestCase):
    """
    Test case for Book API endpoints
    """
    
    def setUp(self):
        """
        Set up test data and client
        """
        # Create test users
        self.user1 = User.objects.create_user(
            username='testuser1', 
            email='test1@example.com', 
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='testuser2', 
            email='test2@example.com', 
            password='testpass123'
        )
        
        # Create test authors
        self.author1 = Author.objects.create(name='William S. Vincent')
        self.author2 = Author.objects.create(name='Eric Matthes')
        self.author3 = Author.objects.create(name='Robert C. Martin')
        
        # Create test books
        self.book1 = Book.objects.create(
            title='Django for Beginners',
            publication_year=2020,
            author=self.author1
        )
        
        self.book2 = Book.objects.create(
            title='Python Crash Course',
            publication_year=2019,
            author=self.author2
        )
        
        self.book3 = Book.objects.create(
            title='Clean Code',
            publication_year=2008,
            author=self.author3
        )
        
        # Initialize API client
        self.client = APIClient()
        
        # Book data for testing creation
        self.new_book_data = {
            'title': 'Test Book',
            'author': self.author1.id,
            'publication_year': 2023
        }

    def test_book_list_unauthenticated(self):
        """
        Test that unauthenticated users can access the book list endpoint
        """
        response = self.client.get(reverse('book-list'))
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(len(response.data), 3)

    def test_book_list_authenticated(self):
        """
        Test that authenticated users can access the book list endpoint
        """
        login_successful = self.client.login(username='testuser1', password='testpass123')
        self.assertTrue(login_successful)
        
        response = self.client.get(reverse('book-list'))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_book_list_filter_by_title(self):
        """
        Test filtering books by title
        """
        response = self.client.get(reverse('book-list') + '?title=Django')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Django for Beginners')

    def test_book_list_filter_by_author(self):
        """
        Test filtering books by author name
        """
        response = self.client.get(reverse('book-list') + '?author=Martin')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Clean Code')

    def test_book_list_filter_by_year(self):
        """
        Test filtering books by publication year
        """
        response = self.client.get(reverse('book-list') + '?publication_year=2019')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Python Crash Course')

    def test_book_list_search(self):
        """
        Test searching books
        """
        response = self.client.get(reverse('book-list') + '?search=python')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Python Crash Course')

    def test_book_list_ordering(self):
        """
        Test ordering books
        """
        # Test ascending order by title
        response = self.client.get(reverse('book-list') + '?ordering=title')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data[0]['title'], 'Clean Code')
        
        # Test descending order by publication_year
        response = self.client.get(reverse('book-list') + '?ordering=-publication_year')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data[0]['publication_year'], 2020)

    def test_book_detail_view(self):
        """
        Test retrieving a single book's details
        """
        response = self.client.get(reverse('book-detail', kwargs={'pk': self.book1.pk}))
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Django for Beginners')

    def test_book_create_authenticated(self):
        """
        Test creating a book as an authenticated user
        """
        login_successful = self.client.login(username='testuser1', password='testpass123')
        self.assertTrue(login_successful)
        
        response = self.client.post(
            reverse('book-create'),
            data=json.dumps(self.new_book_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 4)
        self.assertEqual(response.data['title'], 'Test Book')
        self.assertEqual(response.data['publication_year'], 2023)
        self.assertEqual(response.data['author'], self.author1.id)

    def test_book_create_unauthenticated(self):
        """
        Test that unauthenticated users cannot create books
        """
        response = self.client.post(
            reverse('book-create'),
            data=json.dumps(self.new_book_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Book.objects.count(), 3)

    def test_book_update_authenticated(self):
        """
        Test updating a book as an authenticated user
        """
        login_successful = self.client.login(username='testuser1', password='testpass123')
        self.assertTrue(login_successful)
        
        update_data = {
            'title': 'Updated Book Title',
            'author': self.author2.id,
            'publication_year': 2024
        }
        
        # Test PUT method (complete update)
        response = self.client.put(
            reverse('book-update', kwargs={'pk': self.book1.pk}),
            data=json.dumps(update_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Updated Book Title')
        self.assertEqual(self.book1.author.id, self.author2.id)
        self.assertEqual(self.book1.publication_year, 2024)
        
        # Test PATCH method (partial update)
        partial_update = {'title': 'Partially Updated Title'}
        response = self.client.patch(
            reverse('book-update', kwargs={'pk': self.book1.pk}),
            data=json.dumps(partial_update),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Partially Updated Title')
        self.assertEqual(self.book1.author.id, self.author2.id)

    def test_book_update_unauthenticated(self):
        """
        Test that unauthenticated users cannot update books
        """
        update_data = {'title': 'Should Not Update'}
        response = self.client.put(
            reverse('book-update', kwargs={'pk': self.book1.pk}),
            data=json.dumps(update_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Django for Beginners')

    def test_book_delete_authenticated(self):
        """
        Test deleting a book as an authenticated user
        """
        login_successful = self.client.login(username='testuser1', password='testpass123')
        self.assertTrue(login_successful)
        
        response = self.client.delete(reverse('book-delete', kwargs={'pk': self.book1.pk}))
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 2)
        with self.assertRaises(Book.DoesNotExist):
            Book.objects.get(pk=self.book1.pk)

    def test_book_delete_unauthenticated(self):
        """
        Test that unauthenticated users cannot delete books
        """
        response = self.client.delete(reverse('book-delete', kwargs={'pk': self.book1.pk}))
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Book.objects.count(), 3)