from django.contrib import admin
from django.urls import path
from.import views
urlpatterns = [
    path('',views.index,name='index'),
    path('index.html',views.index,name='index'),
    path('login.html',views.loginn,name='login'),
    path('signup.html',views.signup,name='signup'),
    path('user.html',views.user,name='user'),
    path('logout/',views.logout,name="logout"),
   
]