from django.contrib.auth.models import User  
from django.shortcuts import render, redirect
from .forms import CustomerCreationForm
from django.contrib.auth import logout


# View shown for the homepage
def homepage(request):
    return render(
        request,
        'general/homepage.html'
    )

# View used to delete an account
def delete_account(request):
    print(request.user.id)
    # saving the username of the logged user
    user_id = request.user.id
    # getting the user from the list of users in the db
    u = User.objects.get(id = user_id)

    # logging out the user
    logout(request)      

    # deleting the user
    u.delete()
    return render(
        request,
        'registration/deleteAccount.html'
    )

# View to register a new customer (at the moment the only group available is the customer, eand all the registrations are of type customer)
def registrationCustomer(request):  
    form = CustomerCreationForm()  
    # If the user submits the form, this is saved, passed to the CustomerCreationForm and it's being checked if the form is valid
    if request.method == 'POST':  
        form = CustomerCreationForm(request.POST)  

        # if all the data in the form is correct/valid -> the form is saved -> data is saved in the db -> the user is redirected 
        # to the homepage
        if form.is_valid():  
            form.save()  
            return redirect('/accounts/login')
        
    # when the request.method is of type GET, the form is created and passed to the template
    return render(request, 'registration/registration.html', {
        'form':form  
    })  
