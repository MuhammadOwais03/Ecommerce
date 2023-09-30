from django import forms  # This import is not needed, you can remove it.
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class NewUserRegistration(UserCreationForm):
    email = forms.EmailField(required=True)  # Adds an email field to the form.

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

