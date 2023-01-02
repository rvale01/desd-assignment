from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import CustomerCreationForm

def homepage(request):
    return render(
        request,
        'general/homepage.html'
    )

def registrationCustomer(request):  
    if request.method == 'POST':  
        form = CustomerCreationForm(request.POST)  
        if form.is_valid():  
            form.save()  
            return redirect('/accounts/login')
    else:  
        form = CustomerCreationForm()  
        return render(request, 'registration/registration.html', {
            'form':form  
        })  
