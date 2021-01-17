from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import User, Category, Listing, Bid, Comment

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
    #category = forms.ChoiceField(label="Optional Category", required=False, choices=[<iterable list of tuples ('AA', 'Aaaaaaa')>])


# Views
def index(request):
    return render(request, "auctions/index.html")


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

def create(request):
    if request.method == "POST":
        #Receive form info
        form = CreateListingForm(request.POST)
        if form.is_valid():
            # Use data from form.cleaned_data: e.g., title = form.cleaned_data["title"]
            return HttpResponseRedirect(reverse("index"))
        else:
            # Error message for user about form error:
            return HttpResponseRedirect(reverse("create"))
        pass
    else:
        form = CreateListingForm()
        return render(request, "auctions/create.html", {'form': form})