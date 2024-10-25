from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create/", views.Creating, name="create"),
    path("categories/", views.category, name="category"),
    path("list/<int:id>", views.watchlist, name="watchlist"),
    path("bid/<int:id>", views.Bid, name="bid"),
    path("comment/<int:id>", views.AddComment, name="comment"),
    path("addtowatchlist/<int:id>", views.AddWatchList, name="addwl"),
    path("removefromwatchlist/<int:id>", views.removeWatchList, name="removewl"),
    path("watchlist/", views.realwatchlist, name="realwl"),
    path("end/<int:id>", views.endbid, name="end"),
]  

