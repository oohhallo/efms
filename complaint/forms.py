from django import forms
from .models import Complaint
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
class RegisterComplaintForm(forms.ModelForm):

    class Meta:
        model = Complaint
        fields = ('title', 'description', 'category')

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']