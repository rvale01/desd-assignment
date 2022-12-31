from django.http import JsonResponse
from .models import Showing, Film
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from datetime import datetime

# TODO: split all the functions in different files
@login_required
def showings_list(request, date, time):
    showings = Showing.objects.filter(date=date, time=time)
    return render(
        request,
        'customer/ShowingsList.html',
        {
            'showings': showings,
        }
    )
    
@login_required
def showing_details(request, film_id):
    showing = Showing.objects.get(pk=film_id)
    film = Film.objects.get(pk=showing.pk)
    return render(
        request,
        'customer/ShowingDetails.html',
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


@login_required
def date_selection(request):
    # GET request -> first time the page is loaded
    if(request.method == "GET"):
        timetable = get_showings_dates()
        return render(
            request,
            'customer/DateSelection.html',
            {
                'timetable': timetable
            }
        )
    else: # POST request -> when the user clicks on the select or submits both options
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
                'customer/DateSelection.html',
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
def select_tickets(request, showing_id):
    if(request.method == "GET"): # GET Request -> Page where the user needs to select the tickets
        return render(
                request,
                'customer/TicketsSelection.html',
                {
                    showing_id
                }
            )

def get_total(adults: int, children: int, students: int):
    tot_cost = 0
    if(adults > 0):
        tot_cost+= (8 * adults)
    if(children > 0):
        tot_cost+= (4 * children)
    if(students > 0):
        tot_cost+= (6 * students)
    
    return tot_cost

@login_required
def booking_review(request, showing_id):
    if(request.method == "POST"):
        showing = Showing.objects.get(pk=showing_id)

        adults = int(request.POST.get('adults'))
        children = int(request.POST.get('children'))
        students = int(request.POST.get('students'))
        
        tot_people = adults + children + students
        total = get_total(adults, children, students)

        if(showing.available_seats >= tot_people):
            return render(
            request,
            'customer/BookingReview.html',
            {
                students,
                adults, 
                children,
                showing_id,
                total
            }
        )
        else:
            #display error page
            return render(
                request,
                'customer/NoSpacePage.html'
            )

@login_required
def payment(request):
    if(request.method == "POST"):
        showing_id = request.POST.get('showing_id')
        showing = Showing.objects.get(pk=showing_id)

        adults = int(request.POST.get('adults'))
        children = int(request.POST.get('children'))
        students = int(request.POST.get('students'))
        
        tot_people = adults + children + students
        total = get_total(adults, children, students)

        if(showing.available_seats >= tot_people):
            return render(
            request,
            'customer/BookingReview.html',
            {
                students,
                adults, 
                children,
                showing_id,
                total
            }
        )
        else:
            #display error page
            return render(
                request,
                'customer/NoSpacePage.html'
            )
    else:
        return render(
            request,
            'customer/Payment.html'
        )