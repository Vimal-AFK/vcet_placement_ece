from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from authentication.models import User

class PaperCodeForm(forms.Form):
    paper_code = forms.CharField(max_length=10, required=True)

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['university_number', 'username', 'name', 'email', 'phone_number', 'date_of_birth', 'batch_year', 'section', 'gender']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'batch_year': forms.NumberInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'section': forms.TextInput(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
        }


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Old Password'}),
        label='Old Password'
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'New Password'}),
        label='New Password'
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm New Password'}),
        label='Confirm New Password'
    )
