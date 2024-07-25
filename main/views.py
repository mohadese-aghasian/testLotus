from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Users,User_Like_Blog,Blogs
from .serializers import BlogSerializer,NewBlogSerializer,LikeSerializer
from .forms import BlogForm,CustomUserCreationForm,CustomUserChangeForm,NewBlogForm
from rest_framework import generics,status,permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

import requests
import json
import datetime


# Create your views here.
def home(request):
    return render(request, "home/home.html")

#admin
#123456
def loginview(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        user= authenticate(request,username=username,password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            return render(request,"home/login.html",{"error":"user not found"})
    else:
        return render(request,"home/login.html")

def signin(request):
    message=""
    if request.method=="POST":
        form =CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                form.save()
            except:
                message="somthing went wrong! user didnt saved"
            finally:
                return redirect("login")
    else:
        form=CustomUserCreationForm()
    
    return render(request, "home/signin.html", {"form":form,
                                                "message":message})

# @login_required
class BlogPostList(generics.ListAPIView):
    queryset = Blogs.objects.all()
    serializer_class = BlogSerializer

class LikeAPI(generics.CreateAPIView):
    queryset= User_Like_Blog.objects.all()
    permission_classes=[permissions.IsAuthenticated]
    serializer_class=LikeSerializer

    def get(self, request):
        if request.method=="GET":
            return redirect("blogs")
        
    def put(self, request,*args,**kwargs):
        blog_id = request.data.get('blog_id')
        if not blog_id:
            return Response({'detail': 'Blog ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # blog = generics.get_object_or_404(Blogs, id=blog_id)
        blog=Blogs.objects.get(pk=blog_id)
        like=User_Like_Blog.objects.filter(user=request.user, blog=blog).first()

        if like:
            like.delete()
            return redirect("blogs" )
        else:
            serializer = self.get_serializer(data={'blog': blog.blog_ID, 'user': request.user.id})
            if serializer.is_valid():
                serializer.save(user=request.user)
                return redirect("blogs" )
            return Response("serializer.errors", status=status.HTTP_400_BAD_REQUEST)
        
    def post(self, request,*args,**kwargs):
        if request.POST.get('_method') == 'PUT':
            return self.put(request, *args, **kwargs)
        
        return Response({'detail': 'Method not allowed.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

def ViewBlogs(request):
    if not request.user.is_authenticated:
        return redirect("login")
    response= requests.get("http://127.0.0.1:8000/blogposts/")
    # blogjson= json.dumps(response)
    if response.status_code == 200:
        JsonBlogs = response.json()
        
    return render(request, "home/index.html",{"Blogs":JsonBlogs})

def logoutview(request):
    logout(request)
    return redirect('home')


def add_blog(request):
    if request.method=="POST":
        addform=NewBlogForm(request.POST)
        if addform.is_valid():
            newbloginstance=addform.save(commit=False)
            newbloginstance.author=request.user
            print(newbloginstance)
            newbloginstance.save()
            # return Response(serializer.data, status=status.HTTP_201_CREATED)
            return redirect("blogs")

        else:
            form = NewBlogForm(request.POST)  
    else:
        form = NewBlogForm()
        return render(request, 'home/add.html', {'form': form})

