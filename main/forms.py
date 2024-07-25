from django import forms
from .models import Blogs,Users
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UserChangeForm

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blogs
        fields = ['title', 'content','author']

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Users
        fields = ("email","username","full_name")

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = Users
        fields = ("email","username","full_name", "password")

class NewBlogForm(forms.ModelForm):
    class Meta:
        model=Blogs
        fields = ['title', 'content']

# ori_mohadeseaghasian
# 123456789
# ali_payami
# aaaaaaaaaali3