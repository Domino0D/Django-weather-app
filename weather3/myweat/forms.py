from .models import Profile
from django.contrib.auth.forms import AuthenticationForm
from django import forms 
from django.forms import ModelForm, TextInput
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = 'Temp_scale',
        widgets = {
            'Temp_scale': forms.Select(attrs={'class': 'input'})
        }

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(
            attrs={
                'class': 'input',
                'placeholder': 'Enter your username...'
            }
        )
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                'class': 'input',
                'placeholder': 'Enter your password...'
                
            }
        )
    )
    
class RegisterForm(UserCreationForm):
    username = forms.CharField(
    label="Username",
        widget=forms.TextInput(
            attrs={
                'class': 'input',
                'placeholder': 'Enter your username...'
            }
        )
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                'class': 'input',
                'placeholder': 'Enter your password...'
            }
        )
    ) 
    password2 = forms.CharField(
        label="Password repeat",
        widget=forms.PasswordInput(
            attrs={
                'class': 'input',
                'placeholder': 'Repeat your password...'
            }
        )
    )   
