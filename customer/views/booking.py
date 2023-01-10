from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ..models import Booking, Showing, Film
from .tickets import get_total
from ..forms import TicketsForm

# The function gets as paramters the date and time
@login_required
def showings_list(request, date, time):
    # The showings are filtered by that date and time and in the template there will be shown all the possible showings
    showings = Showing.objects.filter(date=date, time=time)
    return render(
        request,
        'customer/showingsList.html',
        {
            'showings': showings,
            'date': date,
            'time': time
        }
    )

# The function called to show the details of a showing, it gets as parameter the showing_id
@login_required
def showing_details(request, showing_id):
    showing = Showing.objects.get(pk=showing_id) # getting the show based on the showing_id
    film = Film.objects.get(pk=showing.film_id) # getting the fil based on the film_id from of the showing
    return render(
        request,
        'customer/showingDetails.html',
        {
            'showing': showing,
            'film': film
        }
    )


# Function called to get the showing dates, which will then be used to populate a select shown to the user
def get_showings_dates():
    showings = Showing.objects.all()
    timetable = []
    for value in showings:
        # Filtering the showings by just saving those showings with available spaces and saving the date
        if(value.available_seats > 0 and value.date not in timetable):
            timetable.append(value.date)

    return timetable


@login_required
def date_selection(request):
    # GET request -> first time the page is loaded -> show the page with a select where the user is prompt to select a date ONLY
    # among the ones available
    if(request.method == "GET"):
        timetable = get_showings_dates()
        return render(
            request,
            'customer/dateSelection.html',
            {
                'timetable': timetable
            }
        )
    else: # POST request -> when the user selects the date or selects the time
        # if the user has selected the date, and the time is empty
        if(request.POST.get('date') and not request.POST.get('time')):
            # getting the date from the form
            selected_date = request.POST.get('date')
            
            # filtering the showings by the date
            showings = Showing.objects.filter(date=selected_date)
            times = [] # value which will then populate the select with all the times
            timetable = get_showings_dates()

            # looping trough each value in showings
            for value in showings:
                # if there is space in the showing, then the time is added to the list of times
                if(value.available_seats > 0 and value.time not in times):
                    times.append(value.time)
            return render(
                request,
                'customer/dateSelection.html',
                {
                    'times': times,
                    'date': selected_date,
                    'timetable': timetable
                }
            )
        else: 
            # if the user is submitting both the date and the time, the user is 
            # redirected to the page where the details of each showing are displayed
            selected_date = request.POST.get('date')
            selected_time = request.POST.get('time')
            url = 'showings/'+selected_date+'/'+selected_time
            return redirect(url)

# This view is used when showing the user the total cost of the selected tickets
@login_required
def booking_review(request, showing_id):
    # When the request.method is of type POST
    if(request.method == "POST"):
        # The showing based on the showing_id are retrieved
        showing = Showing.objects.get(pk=showing_id)
        # Passing to the tickets form the request received
        form = TicketsForm(request.POST)
        
        # Checking all the data inputted by the user is corret
        if(form.is_valid()):   
            # getting the details from the form
            adults = form.cleaned_data['adults']
            children = form.cleaned_data['children']
            students = form.cleaned_data['students']

            # calculatin the total people, so this will be removed from the available seats
            tot_people = adults + children + students

            # calculating the total the user will have to pay. This is then showed in the template
            total = get_total(adults, children, students)
            
            # If there is enough space, then the template is returned
            if(showing.available_seats >= tot_people):
                print("Username is 2: ", request.user.id)
                # Setting values in the session -> these will be used after the payment is confirmed to save them in the db
                request.session['adults'] = adults
                request.session['children'] = children
                request.session['students'] = students
                request.session['showing_id'] = showing_id
                request.session['username'] = request.user.id

                # Returning the template
                return render(
                request,
                'customer/bookingReview.html',
                {
                    'students': students,
                    'adults': adults, 
                    'children': children,
                    'showing_id': showing_id,
                    'total': total
                }
            )
            else:
                #display error page
                return render(
                    request,
                    'customer/NoSpacePage.html'
                )
        else:
            render(
                request,
                'customer/ticketsSelection.html',
                {
                    'showing_id': showing_id,
                    'form': form
                }
            )
            
        

# This view is used after the user pays and the payment is successful, stripe will redirect the user to this page
@login_required
def success_page(request, checkout_id):
    # Getting values from the session
    adults = request.session.get('adults')
    children = request.session.get('children')
    students = request.session.get('students')
    customer = request.session.get('username')

    # Calculating the total
    total = get_total(adults=adults, children=children, students=students)
    showing_id = request.session.get('showing_id')

    # And how many tickets were booked
    total_people = adults + children + students
    booking = Booking(showing_id = showing_id, quantity = total_people, total = total, customer = customer)
    
    # Updating just one field of the Showing table
    showing = Showing.objects.get(pk=showing_id)
    showing.available_seats = showing.available_seats - total_people
    showing.save(update_fields=['available_seats'])
    
    # Save the new booking in the db
    booking.save()

    # Clearing all the values in the sessions
    request.session['username'] = None
    request.session['adults'] = 0
    request.session['children'] = 0
    request.session['students'] = 0
    request.session['showing_id'] = 0

    return render(
            request,
            'customer/successPage.html'
        )