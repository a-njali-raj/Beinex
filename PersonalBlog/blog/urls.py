from django.conf import settings
from django.conf.urls.static import static
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
    path('addpost.html',views.addpost,name="addpost"),
    path('post_create/', views.post_create, name='post_create'),
    path('myprofile', views.myprofile, name='myprofile'),
    path('edit_post/<int:post_id>/', views.edit_post, name='edit_post'),
    path('delete-post/<int:post_id>/', views.delete_post, name='delete_post'),
    path('update-profile/', views.update_profile, name='update_profile'),
    path('search_results.html', views.search_results, name='search_results'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('post/<int:post_id>/like/',views.like_post, name='like_post'),
    path('validate-username/', views.validate_username, name='validate_username'),
    path('validate-email/', views.validate_email, name='validate_email'),
    path('follow-toggle/<int:user_id>/', views.follow_toggle, name='follow_toggle'),
    ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)