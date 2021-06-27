from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("categories", views.categories, name="categories"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("listing/new", views.newListing, name="newListing"),
    path("listing/<int:listing_id>/bid", views.placeBid, name="placeBid"),
    path("listing/<int:listing_id>/close", views.closeListing, name="closeListing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("watchlist/<int:listing_id>/change", views.change_watchlist, name="change_watchlist"),
    path("listing/<int:listing_id>/comment", views.comment, name="comment")
]
