from django import forms
from .models import User,Note

class UserRegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'age', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }
        
class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content']

