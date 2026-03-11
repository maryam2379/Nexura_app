from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class ExtendedRegisterForm(UserCreationForm):
    email = forms.EmailField(label="Adresse e-mail", required=True)
    telephone = forms.CharField(label="Téléphone", max_length=20, required=True)
    adresse = forms.CharField(label="Adresse de livraison", widget=forms.Textarea(attrs={'rows': 2}), required=True)
    ville = forms.CharField(label="Ville", max_length=100, required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "telephone", "adresse", "ville")

# --- SORTIR CETTE CLASSE DU BLOC PRÉCÉDENT (Alignée à gauche) ---
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control nexura-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control nexura-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-control nexura-input'}),
        }

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['telephone', 'adresse', 'ville']
        widgets = {
            'telephone': forms.TextInput(attrs={'class': 'form-control nexura-input'}),
            'adresse': forms.Textarea(attrs={'class': 'form-control nexura-input', 'rows': 1}),
            'ville': forms.TextInput(attrs={'class': 'form-control nexura-input'}),
        }