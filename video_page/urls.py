from django.urls import path
from . import views

urlpatterns = [

    path('<int:video_id>/', views.video_page, name="video_page"),
    path('savevideo/', views.save_video, name="subscribe"),
    path('togglelike/', views.toggle_like, name="toggle_like")
]
