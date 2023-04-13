from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Category, Listing, Comment


def index(request):
    activelisting = Listing.objects.filter(isActive=True)#isActive in models
    allCategories = Category.objects.all()
    return render(request, "auctions/index.html", {
        "listings": activelisting,
        "categories": allCategories,
    })



def listingdetail(request, id):
    listingData = Listing.objects.get(pk=id)
    isListingInWatchlist = request.user in listingData.watchlist.all()
    allcomments = Comment.objects.filter(listing=listingData)
    return render(request, "auctions/listing.html", {
        "listingdetail": listingData,
        "isListingInWatchlist": isListingInWatchlist,
        "allcomments": allcomments,
    })
    
def addcomment(request, id):
    currentuser = request.user
    listingData = Listing.objects.get(pk=id)
    message = request.POST['newComment'] #get newcomment from the form in listing.html

    newComment = Comment(
        author = currentuser,  #author from Table-Comment in models.py
        listing = listingData, 
        message = message
    )
    
    newComment.save() #save new comment
    
    return HttpResponseRedirect(reverse("listingdetail",args=(id, ))) #listingdetail for the id from listingdetail function


def removewatchlist(request, id):
    listingData = Listing.objects.get(pk=id)
    currentuser = request.user 
    listingData.watchlist.remove(currentuser) 
    return HttpResponseRedirect(reverse("listingdetail",args=(id, ))) #listingdetail for id from listingdetail function

def addwatchlist(request, id):
    listingData = Listing.objects.get(pk=id)
    currentuser = request.user
    listingData.watchlist.add(currentuser)
    return HttpResponseRedirect(reverse("listingdetail",args=(id, )))#listingdetail for id from listingdetail function

def displaywatchlist(request):
    currentuser= request.user
    listings = currentuser.listingwatchlist.all() 
    return render(request, "auctions/watchlist.html",{
        "listings": listings,
    })

def displaycategory(request):    
    if request.method =="POST":
        categoryFromForm = request.POST['category'] # name="category" from select tag (form) in index.html
        category = Category.objects.get(categoryName=categoryFromForm)
        activelisting = Listing.objects.filter(isActive=True, category=category) # 2 category is the category that we want to display
        allCategories = Category.objects.all()
        return render(request, "auctions/index.html", {
            "listings": activelisting, 
            "categories": allCategories,
        })



def createlisting(request): # get data from the List that the viewers created
    if request.method == "GET": # get the Data
        allCategories = Category.objects.all() #get all the Categories in Table Category 
        return render(request, "auctions/createlisting.html", {
            "categories": allCategories # "categories" in {% for category in categories %} in createlisting.html
        })
    else:
        # get the Data from the form in createlisting.html
        title = request.POST["title"] # ["title"] in name="title" in createlisting.html
        description = request.POST["description"]
        imageurl = request.POST["imageurl"]
        price = request.POST["price"]
        category = request.POST["category"]
        #Who is the user
        currentuser = request.user
        # get all the content of category
        categoryData = Category.objects.get(categoryName=category)
        # create a new listing object
        newlisting = Listing( 
            title=title,
            description=description, # 1 description from the models , 2 description from above
            imageUrl=imageurl,
            price=float(price),
            owner = currentuser,
            category=categoryData
        )
        # insert the objects into the Database
        newlisting.save()
        # Redirect new listing to index page
        return HttpResponseRedirect(reverse(index))
        




    
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
