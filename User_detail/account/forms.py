from django import forms
from .models import CustomUser

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'mobile', 'password']

class LoginForm(forms.Form):
    login = forms.CharField(label="Username, Email or Mobile")
    password = forms.CharField(widget=forms.PasswordInput)
