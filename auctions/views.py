from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect 
from django.shortcuts import render,redirect
from django.urls import reverse
from datetime import datetime
from django.contrib import messages
from .models import User, CreateList,Category,AddBidd,Comments
from django.db.models import Max

def index(request):
    Clist = CreateList.objects.all()
    Categories = Category.objects.all()
    return render(request, "auctions/index.html",{
        'Clist': Clist,
        'Categories': Categories,
    })
def Bid(request,id):
    if request.method == 'POST':
        bid = float(request.POST['bid'])
        hidden = request.POST['hidden']
        get = CreateList.objects.get(id=hidden)
        allcomments = Comments.objects.filter(comlist=get)
        getprice = float(get.price)
        if bid > getprice and get.IsActive == True:
            get.price = str(bid)
            get.save()
            Newbid = AddBidd(person=request.user,newbid=bid,bidlist=get.id)
            Newbid.save()
            return HttpResponseRedirect(reverse('watchlist',args=(id, )))
        elif get.IsActive == False:
           return HttpResponseRedirect(reverse('watchlist',args=(id, )))
            
           
        else:
            messages.error(request,"You can't bid less than the actual price")
            return HttpResponseRedirect(reverse('watchlist',args=(id, )))
    return redirect('watchlist')

def endbid(request, id):
    if request.method == 'POST':
        AddBid = AddBidd.objects.all()
        orglist = CreateList.objects.get(pk=id)

        orglist.IsActive = False
        orglist.save()
        return HttpResponseRedirect(reverse('watchlist',args=(id, )))
    else:
        return HttpResponseRedirect(reverse('watchlist',args=(id, )))


def AddComment(request, id):
    if request.method == 'POST':
        comment = request.POST['comment']
        hidden = request.POST['hidden2']
        comlist = CreateList.objects.get(id=hidden)
        allcomments = Comments.objects.filter(comlist=comlist)
        comwriter = Comments(Writer=request.user,comment=comment,comlist=comlist)
        comwriter.save()
        return HttpResponseRedirect(reverse('watchlist',args=(id, )))


    return render(request, "auctions/watchlist.html",{
        'wlist': comlist,
        'allcomments':allcomments

})


def AddWatchList(request,id):
    user = request.user
    addlist = CreateList.objects.get(pk=id)
    addlist.waatchlist.add(user)
    return HttpResponseRedirect(reverse('watchlist',args=(id, )))


def removeWatchList(request,id):
    user = request.user
    addlist = CreateList.objects.get(pk=id)
    addlist.waatchlist.remove(user)
    return HttpResponseRedirect(reverse('watchlist',args=(id, )))


def realwatchlist(request):
    user = request.user
    lists = user.userlist.all()
    return render(request, "auctions/realwatchlist.html",{
      'lists': lists
    })



def watchlist(request, id):    
    Bid = AddBidd.objects.filter(bidlist=id)
    winner = Bid.aggregate(Max('newbid'))
    thewinner = Bid.filter(newbid=winner['newbid__max']).first()
    personn = thewinner.person if thewinner else None
    thislist = CreateList.objects.get(pk=id)
    allcomments = Comments.objects.filter(comlist=thislist)
    itsin = request.user in thislist.waatchlist.all()
    if thislist.IsActive == False   and personn is not None:
        messages.success(request,f"{personn} win this bid")
          
        return render(request, "auctions/watchlist.html",{
                'wlist': thislist,
                'allcomments':allcomments,
                'isit':itsin,
               
                "winner":winner

                })
    elif thislist.IsActive == False   and personn is None:
       messages.success(request,"bid is closed")
        
       return render(request, "auctions/watchlist.html",{
            'wlist': thislist,
            'allcomments':allcomments,
            'isit':itsin,
            
            "winner":winner

            })

    else:
        return render(request, "auctions/watchlist.html",{
        'wlist': thislist,
        'allcomments':allcomments,
        'isit':itsin,
        
        

        })
    






def category(request):
    if request.method == "POST":
        Clist = CreateList.objects.all()
        Categories = Category.objects.all()
        categ = request.POST["category"]
        cat = Category.objects.filter(Category_name=categ)
        
        return render(request, "auctions/category.html",{
'Categories': Categories,
'Cat': categ,
'Clist': Clist
})
        

    return render(request, "auctions/index.html",{
        'Categories': Categories,
        'Clist': Clist
    })

def Creating(request):
    if request.method == 'GET':
        Categories = Category.objects.all()
        return render(request,'auctions/Create.html',{
            'Categories': Categories,
           
        })
    else:
        titlee = request.POST['title']
        describe = request.POST['description']
        url = request.POST['imageurl']
        pricee = request.POST['price']
        categoryy = request.POST['category']
        now = datetime.now()
        categorydata = Category.objects.get(Category_name=categoryy)
        listt = CreateList(title=titlee,description=describe,imageurl=url,price=float(pricee),owner=request.user,category=categorydata,date=f"{now.year}-{now.month}-{now.day}  {now.hour}:{now.minute}")
        listt.save()
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
