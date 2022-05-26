from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
from django.core import validators



class LoginForm(forms.Form):
    username = forms.CharField(required=True ,label='Email', widget=forms.TextInput(attrs={'class':'w3-input w3-border w3-round-small'}),validators=[validators.validate_email])
    password = forms.CharField(required = True,widget=forms.PasswordInput(attrs={'class':'w3-input w3-border w3-round-small'}), validators=[validators.validate_slug])



    