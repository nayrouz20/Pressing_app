from django import forms
from .models import ShippingAdress

class ShippingForm(forms.ModelForm):

    shipping_full_name = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nom et Prénom'}), required=True)   
    shipping_email = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Adresse Email'}), required=True)   
    shipping_address1 = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Adresse 1'}), required=True)   
    shipping_address2 = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Adresse 2'}), required=False)   
    shipping_city = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Cité'}), required=False)   
    shipping_state = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Gouvernorat'}), required=False)   
    shipping_codePostal = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Code Postal'}), required=True)   

    class Meta:
        model = ShippingAdress
        fields = ['shipping_full_name', 'shipping_email', 'shipping_address1', 'shipping_address2', 
                  'shipping_city', 'shipping_state', 'shipping_codePostal']
        exclude = ['user',]
