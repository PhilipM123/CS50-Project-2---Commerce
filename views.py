from datetime import datetime
from email import message
from operator import truediv
from sqlite3 import Timestamp
from time import time
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from .models import Category, User, Auction_Listing, Bids, Comments 
from django.contrib.auth.decorators import login_required
from django.contrib import messages


class NewEntryForm(forms.ModelForm):
    class Meta:
        model = Auction_Listing
        fields = ['title',
                  'price',
                  'content',
                  'pic',
                  ]

    
def index(request):
    return render(request, "auctions/index.html", {
            "listings" : Auction_Listing.objects.all()
        })

def closed_listings(request):
    return render(request, "auctions/closed_listings.html", {
            "listings" : Auction_Listing.objects.all()
        })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return render(request, "auctions/index.html", {
            "listings" : Auction_Listing.objects.all()
        })
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return render(request, "auctions/index.html", {
            "listings" : Auction_Listing.objects.all()
        })


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required(login_url='/login')
def create_listing(request):
    if request.method == "GET":
        return render(request, "auctions/create_listing.html", {
        })

    if request.method == "POST":
        new_listing = Auction_Listing.objects.create(
            title = request.POST.get('title'),
            price = request.POST.get('price'),
            content = request.POST.get('content'),
            pic = request.POST.get('pic'),
            listingdate = datetime.now(),
            user = request.user,
            active = True,
            )
        new_listing.save()
        new_category = Category.objects.create(title = request.POST.get('category'), listing = new_listing) 
        new_category.save()
        
        print(new_category.title)
        return render(request, "auctions/index.html", {
            "listings" : Auction_Listing.objects.all()
        })
        
def single_listing(request, listingid):

    listing = Auction_Listing.objects.filter(id = listingid).first()
    comments = Comments.objects.all()
    category = Category.objects.filter( listing = listing).first()
    category_title = category.title
    return render(request, "auctions/single_listing.html", {
        "listing": listing,
        "comments": comments,
        "category": category_title,
    })

@login_required(login_url='/login')
def add_watchlist(request, listingid):
    listing = Auction_Listing.objects.filter(id = listingid).first()
    user_watchlist = request.user.watchlist

    if listing in user_watchlist.all():
        user_watchlist.remove(listing)
    else:
        user_watchlist.add(listing)
    print("user added or removed to watchlist")

    comments = Comments.objects.all()
    category = Category.objects.filter( listing = listing).first()
    category_title = category.title
    return render(request, "auctions/single_listing.html", {
        "listing": listing,
        "comments": comments,
        "category": category_title,
    })

@login_required(login_url='/login')
def add_bid(request, listingid):

    listing = Auction_Listing.objects.filter(id = listingid).first()
    user = request.user
    userbid = int(request.POST.get('bid', None))
    highestbid = listing.price
    bids = Bids.objects.filter(listing=listing)

    # Get the highest existing bid and set equal to highestbid variable
    if bids is not None:
       for bid in bids:
         if bid.highestbid > highestbid:
            highestbid = bid.highestbid

    # seeing if users price is greater than highestbid and setting them accordingly
    if userbid is not None:
        if userbid > highestbid:
            
            highestbid = userbid
            listing.price = highestbid
            listing.save()
            newbid = Bids.objects.create(highestbid = int(listing.price), listing = listing, user = user)
            newbid.save()
        else:
            messages.error(request, "Error, bid has to exceed current bid")
    
    comments = Comments.objects.all()
    category = Category.objects.filter( listing = listing).first()
    category_title = category.title
    return render(request, "auctions/single_listing.html", {
        "listing": listing,
        "comments": comments,
        "category": category_title,
    })

@login_required(login_url='/login')
def close_listing(request, listingid):
    listing = Auction_Listing.objects.filter(id = listingid).first()
    listing.active = False
    listing.save()

    winningbid = Bids.objects.filter(highestbid = listing.price, listing = listing).first()
    if winningbid:
        winningbid.winner = True
        print(winningbid)
        winningbid.save()
    
    return render(request, "auctions/close_listing.html", {
        "listing": listing,
        "winningbid": winningbid
    })
    
@login_required(login_url='/login')
def comment(request, listingid):
    listing = Auction_Listing.objects.filter(id = listingid).first()
    contents = request.POST.get("comment")
    user = request.user

    newcomment = Comments.objects.create(comment = contents, timestamp = datetime.now(),user = user, listing = listing)
    newcomment.save()

    comments = Comments.objects.all()
    category = Category.objects.filter( listing = listing).first()
    category_title = category.title
    return render(request, "auctions/single_listing.html", {
        "listing": listing,
        "comments": comments,
        "category": category_title,
    })

@login_required(login_url='/login')
def watchlist(request):
    watchlists = Auction_Listing.objects.filter(user_watchlist = request.user)
    listings = watchlists.all()


    return render(request, "auctions/watchlist.html", {
        "listings" : listings
    })

def categories(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {
            "categories" : categories
        })

def category_listings(request, title):
    titles = title
    categories = Category.objects.filter(title=titles)
    

    return render(request, "auctions/category_listings.html", {
            "categories" : categories,
            "title" : titles
        })
