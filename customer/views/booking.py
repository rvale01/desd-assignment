from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ..models import Booking, Showing, Film
from .tickets import get_total
from ..forms import TicketsForm

# DONE !!!
@login_required
def showings_list(request, date, time):
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

@login_required
def showing_details(request, showing_id):
    showing = Showing.objects.get(pk=showing_id) # getting the show based on the f
    film = Film.objects.get(pk=showing.film_id_id)
    return render(
        request,
        'customer/showingDetails.html',
        {
            'showing': showing,
            'film': film
        }
    )



def get_showings_dates():
    showings = Showing.objects.all()
    timetable = []
    for value in showings:
        if(value.available_seats > 0 and value.date not in timetable):
            timetable.append(value.date)

    return timetable


# DONE !!!
@login_required
def date_selection(request):
    # GET request -> first time the page is loaded -> show the page with a select where the user is prompt to select a date 
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
        if(request.POST.get('date') and not request.POST.get('time')):
            selected_date = request.POST.get('date')
            showings = Showing.objects.filter(date=selected_date)
            times = []
            timetable = get_showings_dates()
            for value in showings:
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
            selected_date = request.POST.get('date')
            selected_time = request.POST.get('time')
            url = 'showings/'+selected_date+'/'+selected_time
            return redirect(url)

@login_required
def booking_review(request, showing_id):
    if(request.method == "POST"):
        showing = Showing.objects.get(pk=showing_id)
        form = TicketsForm(request.POST)

        if(form.is_valid()):   
            adults = form.cleaned_data['adults']
            children = form.cleaned_data['children']
            students = form.cleaned_data['students']
            tot_people = adults + children + students
            total = get_total(adults, children, students)

            # Setting values in the session -> these will be used to save them in the db
            request.session['adults'] = adults
            request.session['children'] = children
            request.session['students'] = students
            request.session['showing_id'] = showing_id

            if(showing.available_seats >= tot_people):
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

def success_page(request, checkout_id):
    adults = request.session.get('adults')
    children = request.session.get('children')
    students = request.session.get('students')
    total = get_total(adults=adults, children=children, students=students)
    showing_id = request.session.get('showing_id')
    
    total_people = adults + children + students
    booking = Booking(showing_id = showing_id, quantity = total_people, total = total, customer = request.user.id)
    
    showing = Showing.objects.get(pk=showing_id)
    showing.available_seats = showing.available_seats - total_people
    showing.save(update_fields=['available_seats'])
    
    booking.save()
    return render(
            request,
            'customer/successPage.html'
        )