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
    starting_bid = models.DecimalField(max_digits=12, decimal_places=2)
    current_price = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateTimeField(auto_now=True)
    closed = models.BooleanField(default=False)
    image = models.URLField() #optional
    category = models.CharField(max_length=2) #optional

    def __str__(self):
        return self.title

class Bid(models.Model):
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="bids"
    )
    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE, 
        related_name="bids",
        default="",
    )
    value = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="comments"
    )
    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE, 
        related_name="comments",
        default="",
    )
    text = models.TextField(max_length=1024)
    date = models.DateTimeField(auto_now=True)

class Watchlist(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="watcher"
    )
    item = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        related_name="watching"
    )