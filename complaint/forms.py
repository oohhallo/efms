from django import forms
from .models import Complaint

class RegisterComplaintForm(forms.ModelForm):

    class Meta:
        model = Complaint
        fields = ('title', 'description', 'category')
