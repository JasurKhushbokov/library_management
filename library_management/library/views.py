from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q
from datetime import timedelta
from django.utils import timezone
from .models import Book, Author, Category, BorrowRecord, Wishlist
from .forms import RegistrationForm, BookForm, AuthorForm, CategoryForm

# CI/CD Pipeline: Auto-deployed via GitHub Actions


def is_admin(user):
    return user.is_superuser


def admin_required(view_func):
    return login_required(user_passes_test(is_admin)(view_func))


def home(request):
    books = Book.objects.all()[:6]
    authors = Author.objects.all()[:5]
    categories = Category.objects.all()[:5]
    return render(
        request,
        "library/home.html",
        {"books": books, "authors": authors, "categories": categories},
    )


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect("home")
    else:
        form = RegistrationForm()
    return render(request, "library/register.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, "library/login.html")


def user_logout(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("home")


def book_list(request):
    search_query = request.GET.get("q", "")
    category_id = request.GET.get("category")
    author_id = request.GET.get("author")

    books = Book.objects.all()

    if search_query:
        books = books.filter(
            Q(title__icontains=search_query)
            | Q(isbn__icontains=search_query)
            | Q(description__icontains=search_query)
        )

    if category_id:
        books = books.filter(categories__id=category_id)

    if author_id:
        books = books.filter(author__id=author_id)

    categories = Category.objects.all()
    authors = Author.objects.all()

    return render(
        request,
        "library/book_list.html",
        {"books": books, "categories": categories, "authors": authors},
    )


def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    wishlist_books = []
    if request.user.is_authenticated:
        wishlist = Wishlist.objects.filter(user=request.user).first()
        if wishlist:
            wishlist_books = list(wishlist.books.all())
    return render(
        request,
        "library/book_detail.html",
        {"book": book, "wishlist_books": wishlist_books},
    )


@admin_required
def book_create(request):
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Book created successfully!")
            return redirect("book_list")
    else:
        form = BookForm()
    return render(request, "library/book_form.html", {"form": form, "action": "Create"})


@admin_required
def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, "Book updated successfully!")
            return redirect("book_detail", pk=book.pk)
    else:
        form = BookForm(instance=book)
    return render(request, "library/book_form.html", {"form": form, "action": "Update"})


@admin_required
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        book.delete()
        messages.success(request, "Book deleted successfully!")
        return redirect("book_list")
    return render(request, "library/book_confirm_delete.html", {"book": book})


def author_list(request):
    authors = Author.objects.all()
    return render(request, "library/author_list.html", {"authors": authors})


def author_detail(request, pk):
    author = get_object_or_404(Author, pk=pk)
    books = author.books.all()
    return render(
        request, "library/author_detail.html", {"author": author, "books": books}
    )


@admin_required
def author_create(request):
    if request.method == "POST":
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Author created successfully!")
            return redirect("author_list")
    else:
        form = AuthorForm()
    return render(
        request, "library/author_form.html", {"form": form, "action": "Create"}
    )


@admin_required
def author_update(request, pk):
    author = get_object_or_404(Author, pk=pk)
    if request.method == "POST":
        form = AuthorForm(request.POST, instance=author)
        if form.is_valid():
            form.save()
            messages.success(request, "Author updated successfully!")
            return redirect("author_detail", pk=author.pk)
    else:
        form = AuthorForm(instance=author)
    return render(
        request, "library/author_form.html", {"form": form, "action": "Update"}
    )


@admin_required
def author_delete(request, pk):
    author = get_object_or_404(Author, pk=pk)
    if request.method == "POST":
        author.delete()
        messages.success(request, "Author deleted successfully!")
        return redirect("author_list")
    return render(request, "library/author_confirm_delete.html", {"author": author})


def category_list(request):
    categories = Category.objects.all()
    return render(request, "library/category_list.html", {"categories": categories})


def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    books = category.books.all()
    return render(
        request, "library/category_detail.html", {"category": category, "books": books}
    )


@admin_required
def category_create(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Category created successfully!")
            return redirect("category_list")
    else:
        form = CategoryForm()
    return render(
        request, "library/category_form.html", {"form": form, "action": "Create"}
    )


@admin_required
def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Category updated successfully!")
            return redirect("category_detail", pk=category.pk)
    else:
        form = CategoryForm(instance=category)
    return render(
        request, "library/category_form.html", {"form": form, "action": "Update"}
    )


@admin_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        category.delete()
        messages.success(request, "Category deleted successfully!")
        return redirect("category_list")
    return render(
        request, "library/category_confirm_delete.html", {"category": category}
    )


@login_required
def borrow_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if book.available_copies > 0:
        due_date = timezone.now().date() + timedelta(days=14)
        BorrowRecord.objects.create(user=request.user, book=book, due_date=due_date)
        book.available_copies -= 1
        book.save()
        messages.success(request, f'You have borrowed "{book.title}"')
    else:
        messages.error(request, "No copies available.")
    return redirect("book_detail", pk=pk)


@login_required
def return_book(request, pk):
    record = get_object_or_404(BorrowRecord, pk=pk, user=request.user)
    if record.status == "borrowed":
        record.status = "returned"
        record.returned_at = timezone.now()
        record.save()
        book = record.book
        book.available_copies += 1
        book.save()
        messages.success(request, f'You have returned "{book.title}"')
    return redirect("my_borrowings")


@login_required
def my_borrowings(request):
    records = BorrowRecord.objects.filter(user=request.user).order_by("-borrowed_at")
    return render(request, "library/my_borrowings.html", {"records": records})


@login_required
def wishlist(request):
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    books = wishlist.books.all()
    return render(request, "library/wishlist.html", {"books": books})


@login_required
def add_to_wishlist(request, pk):
    book = get_object_or_404(Book, pk=pk)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)

    if book in wishlist.books.all():
        messages.info(request, f'"{book.title}" is already in your wishlist')
    else:
        wishlist.books.add(book)
        messages.success(request, f'Added "{book.title}" to your wishlist')

    return redirect("book_detail", pk=pk)


@login_required
def remove_from_wishlist(request, pk):
    book = get_object_or_404(Book, pk=pk)
    wishlist = get_object_or_404(Wishlist, user=request.user)

    if book in wishlist.books.all():
        wishlist.books.remove(book)
        messages.success(request, f'Removed "{book.title}" from your wishlist')

    return redirect("wishlist")
