from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import User, Listing, Bid, Comment, Watchlist

# Djago forms
class CreateListingForm(forms.Form):
    title = forms.CharField(label="Title", max_length=64)
    title.widget.attrs.update({'class' : 'form-control'})
    description = forms.CharField(label="Description", widget=forms.Textarea)
    description.widget.attrs.update({'class' : 'form-control'})
    starting_bid = forms.DecimalField(label="Starting bid", max_digits=10, decimal_places=2)
    starting_bid.widget.attrs.update({'class' : 'form-control'})
    image_url = forms.URLField(label="Optional Image URL", required=False)
    image_url.widget.attrs.update({'class' : 'form-control'})

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

    category = forms.ChoiceField(
        label="Optional Category", 
        required=False, 
        choices=CATEGORY_CHOICES
    )


# Views
def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all(),
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
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


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

@login_required(login_url='login')
def create(request):
    if request.method == "POST":
        # Receive form info
        form = CreateListingForm(request.POST)
        if form.is_valid():
            # Use data from form.cleaned_data
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            starting_bid = form.cleaned_data["starting_bid"]
            image_url = form.cleaned_data["image_url"]
            listing = Listing(
                author=request.user,
                title=title, 
                description=description,
                price=starting_bid,
                image=image_url,
            )
            listing.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            # Error message for user about form error:
            return HttpResponseRedirect(reverse("create"))
        pass
    else:
        form = CreateListingForm()
        return render(request, "auctions/create.html",
            {
                'form': form
            }
        )
    
def item(request, item_id):
    listing = Listing.objects.get(id=item_id)
    watchlist_flag = False
    if request.user.is_authenticated:
        watchlist_flag = len(
            Watchlist.objects
            .filter(user=request.user)
            .filter(item=listing)
        )
    return render(request, 'auctions/item.html', {
        'item': listing,
        'watchlist_flag': watchlist_flag,
    })

@login_required(login_url='login')
def watch(request, item_id):
    listing = Listing.objects.get(id=item_id)
    watching = Watchlist.objects.filter(user=request.user).filter(item=listing)
    if len(watching) > 0:
        #Must exclude item from db
        watching.delete()
        pass
    else:
        #must include item in db
        watching = Watchlist(user=request.user, item=listing)
        watching.save()
        pass
    return HttpResponseRedirect(reverse("item", args=(item_id,)))

@login_required(login_url='login')
def watchlist(request):
    watchlists = Watchlist.objects.filter(user=request.user)
    return render(request, 'auctions/watchlist.html', {
        'watchlists': watchlists,
    })