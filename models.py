from tkinter import CASCADE
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
   pass

class Auction_Listing(models.Model):
    title = models.CharField(max_length=30)
    price = models.IntegerField()
    content = models.CharField(max_length=100)
    pic = models.URLField(blank=True)
    listingdate = models.DateTimeField()
    user = models.ForeignKey(User,on_delete=models.CASCADE, null=True)
    user_watchlist = models.ManyToManyField(User, blank=True, related_name="watchlist")
    active = models.BooleanField(blank=True, default=True)

class Bids(models.Model):
    highestbid = models.IntegerField()
    listing = models.ForeignKey(Auction_Listing, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    winner = models.BooleanField(default=False)

class Comments(models.Model):
    comment = models.CharField(max_length=70)
    timestamp = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    listing = models.ForeignKey(Auction_Listing, on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ('-timestamp',)

class Category(models.Model):
    title = models.CharField(max_length=30)
    listing = models.ForeignKey(Auction_Listing, on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ('title',)
