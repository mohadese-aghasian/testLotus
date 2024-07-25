from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Users(AbstractUser):
    # user_ID=models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=128)

# class Users(models.Model):
#     user_ID=models.AutoField(primary_key=True)
#     full_name = models.CharField(max_length=128)
#     created_at=models.DateTimeField(auto_now_add=True)


    def __str__(self) -> str:
        return f"{self.full_name}"
    
class Blogs(models.Model):
    blog_ID=models.AutoField(primary_key=True)
    title=models.CharField(max_length=255)
    content=models.TextField()
    author=models.ForeignKey(Users,on_delete=models.CASCADE,related_name='blogs')
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.blog_ID} : {self.title} by {self.author}, created at {self.created_at}"

class User_Like_Blog(models.Model):
    user=models.ForeignKey(Users, on_delete=models.CASCADE, related_name="user_likes")
    blog=models.ForeignKey(Blogs, on_delete=models.CASCADE, related_name="like_counts")
    liked_at=models.DateTimeField(auto_now=True)

    class Meta:
        unique_together=("blog","user")

    def __str__(self) -> str:
        return f"'{self.user}'  likes '{self.blog}' at '{self.liked_at}'"
    

    