from django.urls import path
from . import views

urlpatterns = [
    path("payment", views.payment, name="payment"),
    path("success_page/<str:checkout_id>", views.success_page, name="payment"),
    path("booking-review/<str:showing_id>", views.booking_review, name="booking_review"), #booking confirmation with id of booking, id of customer
    path("showings/<str:date>/<str:time>", views.showings_list, name="showings_list"), 
    path("showing_details/<str:film_id>", views.showing_details, name="showing details"), 
    path("select-date-showings", views.date_selection),
    path("select_tickets/<str:showing_id>", views.select_tickets),
]
