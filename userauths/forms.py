from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauths.models import User

class UserRegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Username"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Email"}))
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"placeholder": "Password"}),
    )
    password2 = forms.CharField(
        label="Confirm Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password"}),
    )
    
    
    first_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "First Name"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Last Name"}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Phone Number"}))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone_number']
