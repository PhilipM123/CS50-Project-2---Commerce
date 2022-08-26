from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("single_listing/<str:listingid>", views.single_listing, name="single_listing"),
    path("add_watchlist/<str:listingid>", views.add_watchlist, name="add_watchlist"),
    path("add_bid/<str:listingid>", views.add_bid, name="add_bid"),
    path("close_listing/<str:listingid>", views.close_listing, name="close_listing"),
    path("closed_listings", views.closed_listings, name="closed_listings"),
    path("comment/<str:listingid>", views.comment, name="comment"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("category_listings<str:title>", views.category_listings, name="category_listings"),
]
