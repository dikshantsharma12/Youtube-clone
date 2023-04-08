from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name = 'home'),
    path('subscriptions/',views.subscriptions,name="subscriptions"),
    path('history/',views.history,name="subscriptions"),
    path('watchlater/',views.watch_later,name="subscriptions"),
    path('likedvideos/',views.liked_videos,name="subscriptions")
    
]