import email
from django import forms
from .models import User, Tutor, Club, Course

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'second_name', "email", "password", 'course']


#student_id = models.IntegerField(primary_key=True)
    # email = models.EmailField(max_length=254, unique=True)
    # password = models.CharField(max_length=16)
    # is_superuser = models.IntegerField()

    # first_name = models.CharField(max_length=2**10, default="")
    # second_name = models.CharField(max_length=2**10, default="")

    # course