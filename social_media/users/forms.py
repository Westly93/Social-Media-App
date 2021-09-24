from django import forms
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    email= forms.EmailField()
    class Meta:
        model= User 
        fields= ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email= forms.EmailField()
    

    class Meta:
        model= User 
        fields= ['email', 'username']


class ProfileUpdateForm(forms.ModelForm):
    bio= forms.CharField(widget= forms.Textarea(attrs={
        'rows': 3
    }))
    class Meta:
        model= Profile 
        fields= ['bio', 'current_city', 'image']