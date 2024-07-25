from .models import Users,Blogs,User_Like_Blog
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta: 
        model= Users
        fields= ["id","full_name"]
    

class BlogSerializer(serializers.ModelSerializer):
    like_count=serializers.IntegerField(source="like_counts.count", read_only=True)
    author=UserSerializer()

    class Meta:
       model = Blogs
       fields = ["blog_ID","title","content","author","created_at","like_count"]

class NewBlogSerializer(serializers.ModelSerializer):
    class Meta:
        model=Blogs
        fields = ['blog_ID', 'title', 'content', 'author', 'created_at']
        read_only_fields = ['author', 'created_at']

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model=User_Like_Blog
        fields=['user','blog']
        # read_only_fields=['liked_at']
