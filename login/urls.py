from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('login/password_page/', views.password_page, name="password"),
    path('signup/', views.signup, name="signup"),
    path("logout/",views.logout,name="logout")
]