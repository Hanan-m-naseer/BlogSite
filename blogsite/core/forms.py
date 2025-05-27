from django import forms
from django.contrib.auth.models import User
from .models import Profile, BlogPost

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['contact_number', 'profile_pic']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['contact_number', 'profile_pic']

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'image']