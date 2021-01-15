from django.contrib import admin
from django.urls import include, path
from . import views

app_name = "flights"
urlpatterns = [
    path('', views.index, name="index"),
    path("<int:flight_id>", views.flight, name="flight"),
    path("<int:flight_id>/book", views.book, name="book"),
]