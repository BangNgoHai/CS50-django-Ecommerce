from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createlisting", views.createlisting, name="createlisting"),
    path("displaycategory", views.displaycategory, name="displaycategory"),
    path("listingdeatil/<int:id>", views.listingdetail, name="listingdetail"),
    path("watchlist", views.displaywatchlist, name="watchlist"),
    path("removewatchlist/<int:id>", views.removewatchlist, name="removewatchlist"),
    path("addwatchlist/<int:id>", views.addwatchlist, name="addwatchlist"),
    path("addcomment/<int:id>", views.addcomment, name="addcomment"),
]
