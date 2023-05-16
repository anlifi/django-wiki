from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("edit/<str:title>", views.edit, name="edit"),
    path("new", views.new, name="new"),
    path("search", views.search, name="search"),
    path("<str:title>", views.entry, name="entry"),
]
