from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ..forms import TicketsForm

# Function used to get the total amount of the booking based on the number of tickets for adults, children, and students
def get_total(adults: int, children: int, students: int):
    tot_cost = 0
    if(adults > 0):
        tot_cost+= (8 * adults)
    if(children > 0):
        tot_cost+= (4 * children)
    if(students > 0):
        tot_cost+= (6 * students)
    
    return tot_cost

# View showed to the user so they can choose the different tickets they need
@login_required
def select_tickets(request, showing_id):
    if(request.method == "GET"): # Page where the user needs to select the tickets
        form = TicketsForm()
        return render(
                request,
                'customer/ticketsSelection.html',
                {
                    'showing_id': showing_id,
                    'form': form
                }
            )