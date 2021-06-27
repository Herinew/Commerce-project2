from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from .models import Listings, Bids, Comments, User, Category
from .forms import newListingsForm, newBidsForm, newCommentsForm
from django.contrib.auth.decorators import login_required


def index(request):
    return activeListing(request)


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
        return render(request, "auctions/login.html", {
            "login": "active"
        })


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
        return render(request, "auctions/register.html", {
            "register": "active"
        })


def listing(request, listing_id):
    listing = Listings.objects.get(id=listing_id)
    watchers = listing.watchers.all()
    form = newBidsForm()
    commentsForm = newCommentsForm()
    bid = Bids.objects.filter(auctions=listing).count()
    comments = Comments.objects.filter(listing=listing)
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "form": form,
        "bid": bid,
        "watchers": watchers,
        "commentsForm": commentsForm,
        "comments": comments
    })


@login_required
def newListing(request):
    created = False
    if request.method == "POST":
        user = Listings(user=request.user)
        form = newListingsForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/listing/new?created=True')
    else:
        form = newListingsForm()
        if 'created' in request.GET:
            created = True
    return render(request, "auctions/newlisting.html", {
        "form": form,
        "created": created,
        "newListing": "active"
    })


@login_required
def placeBid(request, listing_id):
    listing = Listings.objects.get(id=listing_id)
    offer = float(request.POST['offers'])
    bid = Bids.objects.filter(auctions=listing)
    if offer >= listing.startingBid and (listing.currentBid is None or offer > listing.currentBid):
        listing.currentBid = offer
        form = newBidsForm(request.POST)
        bid = form.save(commit=False)
        bid.auctions = listing
        bid.user = request.user
        bid.save()
        listing.save()
        return HttpResponseRedirect(reverse("listing", args=[listing_id]))
    else:
        return render(request, "auctions/listing.html", {
            "form": newBidsForm(),
            "listing": listing,
            "error": True,
            "bid": bid.count()
        })

# Pendiente cerrar auction sin haber bids
@login_required
def closeListing(request, listing_id):
    listing = Listings.objects.get(id=listing_id)
    if listing.currentBid is not None:   
        if listing.user == request.user:
            listing.isActive = False
            listing.buyer = Bids.objects.filter(auctions=listing).last().user
            listing.save()
            return HttpResponseRedirect(reverse('listing', args=[listing_id]))
        

@login_required
def watchlist(request):
    listings = request.user.watched_listing.all()
    return render(request, "auctions/watchlist.html", {
        "listings": listings,
        "watchlist": "active"
    })
    

@login_required
def change_watchlist(request, listing_id):
    listing = Listings.objects.get(id=listing_id)
    if request.user in listing.watchers.all():
        listing.watchers.remove(request.user)
    else:
        listing.watchers.add(request.user)
    return HttpResponseRedirect(reverse('watchlist'))
    

def activeListing(request):
    category_id = request.GET.get("category", None)
    if category_id is None:
        listings = Listings.objects.filter(isActive=True)
        category = "Active Listings"
    else:
        listings = Listings.objects.filter(isActive=True, category=category_id)
        category = Category.objects.get(id=category_id)
    return render(request, "auctions/index.html", {
        "listings": listings,
        "category": category,
        "index": "active"
    })


@login_required
def categories(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {
        "categories": categories,
        "categories_active": "active"
    })


@login_required
def comment(request, listing_id):
    listing = Listings.objects.get(id=listing_id)
    form = newCommentsForm(request.POST)
    newComment = form.save(commit=False)
    newComment.user = request.user
    newComment.listing = listing
    newComment.save()
    return HttpResponseRedirect(reverse('listing', args=[listing_id]))
