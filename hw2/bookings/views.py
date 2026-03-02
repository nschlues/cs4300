from django.shortcuts import render, get_object_or_404
from .models import Movie 

# Seat View
def SeatViewSet(request, ):

# Booking View 
def BookingViewSet(request, movie, user):

    return render(request, 'book_seats.html', {'movie'})

# Movie View
def MovieViewSet():
    