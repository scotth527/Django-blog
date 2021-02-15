from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
import datetime
#from django.contrib.auth import LoginView

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    address = forms.CharField(max_length=30, required=True)
    city = forms.CharField(max_length=30, required=True)
    state = forms.CharField(max_length=30, required=True)
    birthday = forms.DateField(initial=datetime.date.today, required=True, widget=forms.SelectDateWidget())
    email = forms.EmailField(max_length=254, required=True, widget=forms.TextInput(attrs={'placeholder': 'E.g. example@aol.com'}) )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

