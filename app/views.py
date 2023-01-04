from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import CustomerCreationForm

# View shown for the homepage
def homepage(request):
    return render(
        request,
        'general/homepage.html'
    )

# View to register a new customer (at the moment the only group available is the customer, eand all the registrations are of type customer)
def registrationCustomer(request):  
    # If the user submits the form, this is saved, passed to the CustomerCreationForm and it's being checked if the form is valid
    if request.method == 'POST':  
        form = CustomerCreationForm(request.POST)  

        # if all the data in the form is correct/valid -> the form is saved -> data is saved in the db -> the user is redirected 
        # to the homepage
        if form.is_valid():  
            form.save()  
            return redirect('/accounts/login')
    else:  
        # when the request.method is of type GET, the form is created and passed to the template
        form = CustomerCreationForm()  
        return render(request, 'registration/registration.html', {
            'form':form  
        })  
