from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import SetPasswordForm, UserCreationForm
from dryWashing.models import Profile

class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

class ChangePasswordForm(SetPasswordForm):
    class Meta:
        model = User
        fields = ['new_password1', 'new_password2']

# Formulaire d'inscription avec les mêmes champs que CustomUserChangeForm
class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(
        required=True, 
        label="Prénom", 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez votre prénom'})
    )
    last_name = forms.CharField(
        required=True, 
        label="Nom de famille", 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entrez votre nom'})
    )
    email = forms.EmailField(
        required=True, 
        label="Adresse e-mail", 
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Entrez votre adresse e-mail'})
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class UserInfoForm(forms.ModelForm):
        phone = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Phone'}), required=False)
        address1 = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'address1'}), required=False)
        address2 = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'address2'}), required=False)
        city = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'city'}), required=False)
        state = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'state'}), required=False)
        codePostal = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'codePostal'}), required=False)
        class Meta:
            model = Profile
            fields = ('phone', 'address1', 'address2', 'city','state', 'codePostal')

