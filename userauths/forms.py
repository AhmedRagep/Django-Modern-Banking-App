from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class UsreRegisterForm(UserCreationForm):

  class Meta:
    model = User
    fields = ['username', 'email', 'password1', 'password2']