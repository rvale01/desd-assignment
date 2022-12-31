from django import forms
from .models import Showing 

#TODO: Ticket -> Student, Child, Adult
class DateSelectionForm(forms.ModelForm):
    class Meta:
        model = Showing
        fields = ("date", "time",)   
