from django.urls import path
from .views.booking import booking_review, date_selection, showing_details, showings_list, success_page
from .views.payment import payment
from .views.tickets import select_tickets

urlpatterns = []

# Payment views
urlpatterns += [
    path("payment", payment, name="payment"),
]

# Booking Views
urlpatterns += [
    path("success_page/<str:checkout_id>", success_page, name="payment"),
    path("booking-review/<str:showing_id>", booking_review, name="booking_review"), #booking confirmation with id of booking, id of customer
    path("showings/<str:date>/<str:time>", showings_list, name="showings_list"), 
    path("showing_details/<str:film_id>", showing_details, name="showing details"), 
    path("select-date-showings", date_selection, name="date_selection"),
]

# Tickets views
urlpatterns += [
    path("select_tickets/<str:showing_id>", select_tickets, name="select_tickets"),
]