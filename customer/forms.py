from django import forms
from .models import Booking 

#TODO: Ticket -> Student, Child, Adult

class Bookingform(forms.ModelForm):
    class Meta:
        model = Booking
        fields=('showing', 'quantity', 'total', 'customer',)