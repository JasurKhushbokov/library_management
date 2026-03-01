from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("books/", views.book_list, name="book_list"),
    path("books/<int:pk>/", views.book_detail, name="book_detail"),
    path("books/create/", views.book_create, name="book_create"),
    path("books/<int:pk>/update/", views.book_update, name="book_update"),
    path("books/<int:pk>/delete/", views.book_delete, name="book_delete"),
    path("books/<int:pk>/borrow/", views.borrow_book, name="borrow_book"),
    path("authors/", views.author_list, name="author_list"),
    path("authors/<int:pk>/", views.author_detail, name="author_detail"),
    path("authors/create/", views.author_create, name="author_create"),
    path("authors/<int:pk>/update/", views.author_update, name="author_update"),
    path("authors/<int:pk>/delete/", views.author_delete, name="author_delete"),
    path("categories/", views.category_list, name="category_list"),
    path("categories/<int:pk>/", views.category_detail, name="category_detail"),
    path("categories/create/", views.category_create, name="category_create"),
    path("categories/<int:pk>/update/", views.category_update, name="category_update"),
    path("categories/<int:pk>/delete/", views.category_delete, name="category_delete"),
    path("my-borrowings/", views.my_borrowings, name="my_borrowings"),
    path("borrow/<int:pk>/return/", views.return_book, name="return_book"),
    path("wishlist/", views.wishlist, name="wishlist"),
    path("wishlist/add/<int:pk>/", views.add_to_wishlist, name="add_to_wishlist"),
    path(
        "wishlist/remove/<int:pk>/",
        views.remove_from_wishlist,
        name="remove_from_wishlist",
    ),
]
