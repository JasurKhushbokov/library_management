from django.contrib import admin
from .models import Author, Category, Book, BorrowRecord, Wishlist


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ["name", "date_of_birth"]
    search_fields = ["name", "biography"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name", "description"]


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "isbn", "available_copies", "published_date"]
    list_filter = ["categories", "author", "published_date"]
    search_fields = ["title", "isbn", "description"]
    filter_horizontal = ["categories"]


@admin.register(BorrowRecord)
class BorrowRecordAdmin(admin.ModelAdmin):
    list_display = ["user", "book", "borrowed_at", "due_date", "returned_at", "status"]
    list_filter = ["status", "borrowed_at", "due_date"]
    search_fields = ["user__username", "book__title"]
    date_hierarchy = "borrowed_at"


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ["user", "created_at"]
    filter_horizontal = ["books"]
