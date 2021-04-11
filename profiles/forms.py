from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
import datetime
#from django.contrib.auth import LoginView
from .models import Friendship

STATUS_CHOICES = (
                  ("Accept", "Accept"),
                  ("Decline", "Decline"))

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

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        ## add a "form-control" class to each form input
        ## for enabling bootstrap
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })

class FriendshipRequestForm(forms.ModelForm):
    class Meta:
        model = Friendship
        fields = ('status',)

    def __init__(self, *args, **kwargs):
        super(FriendshipRequestForm, self).__init__(*args, **kwargs)
        ## add a "form-control" class to each form input
        ## for enabling bootstrap
        for name in self.fields.keys():
            self.fields[name].widget.attrs.update({
                'class': 'form-control',
            })

class FriendshipUpdateForm(forms.ModelForm):
      status = forms.CharField(max_length=30, widget=forms.Select(choices=STATUS_CHOICES), required=True)

      class Meta:
          model = Friendship
          fields = ('status',)

      def __init__(self, *args, **kwargs):
          super(FriendshipUpdateForm, self).__init__(*args, **kwargs)
          ## add a "form-control" class to each form input
          ## for enabling bootstrap
          for name in self.fields.keys():
              self.fields[name].widget.attrs.update({
                  'class': 'form-control',
              })


