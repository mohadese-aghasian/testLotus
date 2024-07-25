from django.urls import path
from . import views

urlpatterns=[
    path("",views.home, name="home"),
    path('blogposts/', views.BlogPostList.as_view(), name='blogpost-list'),
    path("viewblogs/", views.ViewBlogs, name="blogs"),
    path("viewblogs/addnew/",views.add_blog, name="addblog"),
    path("login/",views.loginview, name="login"),
    path('logout/', views.loginview, name="logout"),
    path("signin/",views.signin, name="signin"), 
    path("like/<int:blog_id>/", views.LikeAPI.as_view(), name="like"),
    path("like/", views.LikeAPI.as_view(), name="like"),
   
    
    
]