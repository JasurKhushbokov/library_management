from django.contrib import admin
from django.utils.html import format_html
from .models import Author, Category, Book, BorrowRecord, Wishlist


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ["name", "date_of_birth", "book_count"]
    search_fields = ["name", "biography"]
    list_filter = ["date_of_birth"]
    readonly_fields = ["book_count"]

    fieldsets = (
        ("Basic Information", {"fields": ("name", "date_of_birth")}),
        ("Biography", {"fields": ("biography",), "classes": ("collapse",)}),
    )

    def book_count(self, obj):
        return obj.books.count()

    book_count.short_description = "Books"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "book_count", "description_preview"]
    search_fields = ["name", "description"]

    def description_preview(self, obj):
        return (
            obj.description[:50] + "..."
            if len(obj.description) > 50
            else obj.description
        )

    description_preview.short_description = "Description"

    def book_count(self, obj):
        return obj.books.count()

    book_count.short_description = "Books"


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "author",
        "isbn",
        "available_copies",
        "published_date",
        "cover_thumbnail",
    ]
    list_filter = ["categories", "author", "published_date", "available_copies"]
    search_fields = ["title", "isbn", "description"]
    filter_horizontal = ["categories"]
    readonly_fields = ["cover_thumbnail"]
    date_hierarchy = "published_date"

    fieldsets = (
        ("Basic Information", {"fields": ("title", "isbn", "author")}),
        (
            "Publication Details",
            {
                "fields": (
                    "published_date",
                    "description",
                    "cover_image",
                    "cover_thumbnail",
                )
            },
        ),
        ("Availability", {"fields": ("available_copies",)}),
        ("Categories", {"fields": ("categories",)}),
    )

    def cover_thumbnail(self, obj):
        if obj.cover_image:
            return format_html(
                '<img src="{}" style="width: 50px; height: 70px; object-fit: cover; border-radius: 4px;">',
                obj.cover_image.url,
            )
        return "-"

    cover_thumbnail.short_description = "Cover"


@admin.register(BorrowRecord)
class BorrowRecordAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "book",
        "borrowed_at",
        "due_date",
        "returned_at",
        "status_badge",
    ]
    list_filter = ["status", "borrowed_at", "due_date"]
    search_fields = ["user__username", "book__title"]
    date_hierarchy = "borrowed_at"
    readonly_fields = ["borrowed_at"]

    def status_badge(self, obj):
        colors = {
            "borrowed": "info",
            "returned": "success",
            "overdue": "danger",
        }
        return format_html(
            '<span class="badge badge-{}">{}</span>',
            colors.get(obj.status, "info"),
            obj.get_status_display(),
        )

    status_badge.short_description = "Status"

    fieldsets = (
        ("Borrow Information", {"fields": ("user", "book", "borrowed_at", "due_date")}),
        ("Return Information", {"fields": ("returned_at", "status")}),
    )


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ["user", "book_count", "created_at"]
    filter_horizontal = ["books"]

    def book_count(self, obj):
        return obj.books.count()

    book_count.short_description = "Books"
