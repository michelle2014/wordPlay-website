from django.urls import path, re_path
from . import views

urlpatterns = [
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new", views.new, name="new"),
    path("create_category", views.create_category, name="create_category"),
    path("", views.index, name="index"),
    path("category/<str:category>", views.index, name="index"),
    path("trending_quotes", views.trending_quotes, name="trending_quotes"),
    path("trending_words", views.trending_words, name="trending_words"),
    path("upload", views.upload, name="upload"),
    path("search", views.search, name="search"),
    path("about", views.about, name="about"),
    path("download", views.download, name="download"),
    path("<str:username>", views.profile, name="profile"),
    path("<str:username>/words", views.words_view, name="words_view"),
    path("<str:username>/bookmarks", views.bookmarks_view, name="bookmarks_view"),
    path("word/<str:word_id>", views.word, name="word"),
    path("add_quotation/<int:word_id>", views.add_quotation, name="add_quotation"),
    path("quotations/<int:word_id>", views.quotations, name="quotations"),
    path("edit/<int:word_id>", views.edit, name="edit"),
    path("delete/<int:word_id>", views.delete, name="delete"),
    path("<str:username>/leaderboard", views.leaderboard, name="leaderboard"),
    path("<str:username>/likes", views.likes_view, name="likes_view"),
    path("<str:username>/likeds", views.likeds_view, name="likeds_view"),
    # API Routes
    path(
        "add_bookmarks/<int:word_id>/<int:user_id>",
        views.add_bookmarks,
        name="add_bookmarks",
    ),
    path("likes/<int:quotation_id>/<int:user_id>", views.likes, name="likes"),
]
