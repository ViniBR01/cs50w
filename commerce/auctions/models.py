from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Listing(models.Model):
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="listings"
    )
    title = models.CharField(max_length=64)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateTimeField(auto_now=True)
    closed = models.BooleanField(default=False)
    image = models.URLField() #optional
    category = models.CharField(max_length=2) #optional

class Bid(models.Model):
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="bids"
    )
    value = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="comments"
    )
    text = models.TextField(max_length=1024)
    date = models.DateTimeField(auto_now=True)

#todo: a class for watchlists