from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    watchlist = models.ManyToManyField(Listing, blank=True, related_name="watchers")

class Category(models.Model):
    NOT_DEFINED = 'ND'
    CLOTHING = 'CL'
    BOOKS = 'BK'
    ELECTRONICS = 'EL'
    HOME = 'HM'
    FOOD = 'FD'
    BEAUTY = 'BE'
    TOYS = 'TY'
    SPORTS = 'SP'
    AUTOMOTIVE = 'AT'
    CATEGORY_CHOICES = [
        (NOT_DEFINED, 'Not defined'),
        (CLOTHING, 'Clothing, Shoes, Jewelry and Watches'),
        (BOOKS, 'Books and School Suplies'),
        (ELECTRONICS, 'Electronics and Computers'),
        (HOME, 'Home, Garden and Tools'),
        (FOOD, 'Food and Groceries'),
        (BEAUTY, 'Beauty and Health'),
        (TOYS, 'Toys, Kids and Baby'),
        (SPORTS, 'Sports and Outdoors'),
        (AUTOMOTIVE, 'Automotive and Industrial'),
    ]
    title = models.CharField(
        max_length=2,
        choices=CATEGORY_CHOICES,
        default=NOT_DEFINED,
    )

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField() #fix-me
    price = models.DecimalField(decimal_places=2)
    date = models.DateTimeField(auto_now=True)
    closed = models.BooleanField(default=False)
    image = models.URLField() #optional
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        related_name="listings",
    ) #optional
    pass

class Bid(models.Model):
    pass

class Comment(models.Model):
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="comments"
    )
    text = models.TextField(max_length=1024)
    date = models.DateTimeField(auto_now=True)