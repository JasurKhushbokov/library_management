from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    name = models.CharField(max_length=200)
    biography = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    isbn = models.CharField(max_length=13, unique=True)
    published_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)
    cover_image = models.ImageField(upload_to="covers/", null=True, blank=True)
    available_copies = models.PositiveIntegerField(default=1)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")
    categories = models.ManyToManyField(Category, related_name="books")

    def __str__(self):
        return self.title


class BorrowRecord(models.Model):
    STATUS_CHOICES = [
        ("borrowed", "Borrowed"),
        ("returned", "Returned"),
        ("overdue", "Overdue"),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="borrow_records"
    )
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name="borrow_records"
    )
    borrowed_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField()
    returned_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="borrowed")

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"


class Wishlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="wishlist")
    books = models.ManyToManyField(Book, related_name="wishlisted_by")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Wishlist"
