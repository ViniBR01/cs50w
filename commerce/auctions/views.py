from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import User, Listing, Bid, Comment, Watchlist

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

    category = forms.ChoiceField(
        label="Optional Category", 
        required=False, 
        choices=CATEGORY_CHOICES
    )

class BiddingForm(forms.Form):
    bid_value = forms.DecimalField(label="Your bid", max_digits=10, decimal_places=2)
    bid_value.widget.attrs.update({'class' : 'form-control'})

class CommentForm(forms.Form):
    text = forms.CharField(label="Comment", max_length=200, widget=forms.Textarea)
    text.widget.attrs.update({'class' : 'form-control'})

# Views
def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(closed=False),
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
            category = form.cleaned_data["category"]
            listing = Listing(
                author=request.user,
                title=title, 
                description=description,
                starting_bid=starting_bid,
                current_price=starting_bid,
                image=image_url,
                category=category,
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
    message = ""
    #Fix-me: should not have a current price field. Should get current price from bids
    price = 0
    bids = Bid.objects.filter(listing=listing).order_by('date')
    n_bids = len(bids)
    if n_bids == 0:
        price = listing.starting_bid
    else:
        price = bids[0].value
    Listing.objects.filter(id=item_id).update(current_price=price)

    if request.method == "POST":
        form = BiddingForm(request.POST)
        if form.is_valid():
            # Use data from form.cleaned_data
            bid_value = form.cleaned_data["bid_value"]
            if bid_value >= listing.starting_bid and bid_value > listing.current_price:
                Listing.objects.filter(id=item_id).update(current_price=bid_value)
                listing = Listing.objects.get(id=item_id)
                bid = Bid(
                    author=request.user,
                    listing=listing,
                    value=bid_value,
                )
                bid.save()
                message = "Successfuly received your bid"
            else:
                message = "Error: Your bid must be equal to the initial bid and larger than the previous"

    watchlist_flag = False
    owner_flag = False
    if request.user.is_authenticated:
        watchlist_flag = len(
            Watchlist.objects
            .filter(user=request.user)
            .filter(item=listing)
        )
        if listing.author == request.user:
            owner_flag = True
    bidding_form = BiddingForm()
    comment_form = CommentForm()
    comments = Comment.objects.filter(listing=listing)
    return render(request, 'auctions/item.html', {
        'item': listing,
        'message': message,
        'watchlist_flag': watchlist_flag,
        'owner_flag': owner_flag,
        'bidding_form': bidding_form,
        'comments': comments,
        'comment_form': comment_form,
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
def close(request, item_id):
    #Here, check if user is the owner and update status to closed=True
    return HttpResponseRedirect(reverse("item", args=(item_id,)))

@login_required(login_url='login')
def comment(request, item_id):
    listing = Listing.objects.get(id=item_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        text = form.cleaned_data["text"]
        comment = Comment(author=request.user, listing=listing, text=text)
        comment.save()
    return HttpResponseRedirect(reverse("item", args=(item_id,)))

def categories(request):
    return render(request, 'auctions/categories.html', {
        'categories': CATEGORY_CHOICES,
    })

def categorized(request, cat_id):
    listings = Listing.objects.all().filter(category=cat_id)
    category = ''
    for item in CATEGORY_CHOICES:
        if item[0]==cat_id:
            category = item[1]
    return render(request, 'auctions/categorized.html', {
        'listings': listings,
        'category': category,
    })

@login_required(login_url='login')
def watchlist(request):
    watchlists = Watchlist.objects.filter(user=request.user)
    return render(request, 'auctions/watchlist.html', {
        'watchlists': watchlists,
    })