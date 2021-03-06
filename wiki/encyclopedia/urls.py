from django.urls import path

from . import views

app_name = "wiki"
urlpatterns = [
    path("", views.index, name="index"),
    path("search/<str:search>", views.search, name="search"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("new", views.new, name="new"),
    path("edit", views.edit, name="edit"),
    path("rand", views.rand, name="rand"),
]
