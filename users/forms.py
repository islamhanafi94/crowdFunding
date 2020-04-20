from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import Users

class RegistraionForm(UserCreationForm):
    email = forms.EmailField(help_text="enter your email...")

    class Meta:
        model = Users
        fields = ('email','first_name','last_name','phone','photo','password1','password2')