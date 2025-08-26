from django import forms
from .models import User

class UserRegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'age', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }

