from django import forms  
from django.contrib.auth.models import User, Group  
from django.contrib.auth.forms import UserCreationForm  
from django.core.exceptions import ValidationError  

class CustomerCreationForm(UserCreationForm):  
    username = forms.CharField(label='username', min_length=5, max_length=150)  
    password1 = forms.CharField(label='password', widget=forms.PasswordInput)  
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)  
  
    def username_clean(self):  
        username = self.cleaned_data['username'].lower()  
        user = User.objects.filter(username = username)  
        if user.count():  
            raise ValidationError("Ops! The username already is present in the database! Make sure to use a unique username")  
        return username  
  
    def clean_password2(self):  
        password1 = self.cleaned_data['password1']  
        password2 = self.cleaned_data['password2']  
  
        if password1 and password2 and password1 != password2:  
            raise ValidationError("The two passwords do not match! Try again, please!")  
        return password2  
  
    def save(self):  
        customer_group = Group.objects.get(name='customer') 
        user = User.objects.create_user( 
            username= self.cleaned_data['username'],  
            password= self.cleaned_data['password1'],
        )  
        user.groups.add(customer_group)
        return user  