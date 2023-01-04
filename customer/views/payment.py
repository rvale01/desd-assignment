from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import stripe
from ..models import Showing

# This view is used after the user decides to pay
@login_required
def payment(request):
    if(request.method == "POST"):

        # Getting all the details from the form (the inputs in the template bookingReview are actually hidden, the only reason they are there is to 
        # get the data from one view to the other without using cache, cookies and avoiding using any memory )
        showing_id = request.POST.get('showing_id')
        showing = Showing.objects.get(pk=showing_id)

        adults = int(request.POST.get('adults'))
        children = int(request.POST.get('children'))
        students = int(request.POST.get('students'))
        
        # Calculating the total number of people
        tot_people = adults + children + students

        # Personal API KEY
        stripe.api_key = 'sk_test_51ML6GvA5JuwZl2aDVTNJ2ITAXhbXiGWTJTKbvQVs0eDqnMOn9GTjOB46QGUgR3Ad2kZ664yHFI1OCG0sAneQZyln00n8Zu12I7'
        
        # Passing all the details to the stripe Session create function, which will return the url of a self hosted checkout
        response = stripe.checkout.Session.create(
            mode="payment",
            line_items=[
                {
                "price": "price_1ML6TgA5JuwZl2aD5mmeqnog",
                "quantity": adults,
                },
                {
                "price": "price_1ML6TEA5JuwZl2aDcUXhOsle",
                "quantity": students,
                },
                {
                "price": "price_1ML6TzA5JuwZl2aD4tubjoPl",
                "quantity": children,
                },
            ],
            success_url='http://127.0.0.1:8000/customer/success_page/{CHECKOUT_SESSION_ID}',
            cancel_url= 'http://127.0.0.1:8000',
            payment_method_types = ['card']
        )

        # Re checking if there is enough space in the showing
        if(showing.available_seats >= tot_people):
            return redirect(response.url)
        else:
            #display error page
            return render(
                request,
                'customer/NoSpacePage.html'
            )
    else:
        return render(
            request,
            'customer/NoSpacePage.html'
        )
