from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

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
    CATEGORIES_CHOICES = [
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
        choices=CATEGORIES_CHOICES,
        default=NOT_DEFINED,
    )

class Listing(models.Model):
    pass

class Bid(models.Model):
    pass

class Comment(models.Model):
    pass