from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField() #default: required=True

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


# lets user update username and email
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()  # default: required=True

    class Meta:
        model = User
        fields = ['username', 'email']


# lets user update image
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']