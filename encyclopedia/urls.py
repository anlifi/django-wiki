from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("edit/<str:title>", views.edit, name="edit"),
    path("new", views.new, name="new"),
    path("random", views.random_page, name="random"),
    path("search", views.search, name="search"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("<str:title>", views.redirect_entry, name="redirect_entry"),
]
