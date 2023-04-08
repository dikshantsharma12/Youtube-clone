from django.urls import path
from . import views

urlpatterns = [
    path('profile/<int:profile_id>',views.profile,name="youtuber"),
    path('subscribe_or_unsubscribe/',views.subscribe ,name="subscribe")
]
