import email
from django import forms
from .models import User, Tutor, Club, Course

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'second_name', "email", "password", 'course']