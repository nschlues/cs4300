from django.shortcuts import render, get_object_or_404
from .models import Movie, Seat, Booking 

# Base View
def BaseViewSet(request):
    return render(request, 'bookings/base.html')

# Seat View for seat availability and booking
def SeatViewSet(request):
    seats = Seat.objects.all()
    return render(request, 'bookings/seat_booking.html', {'seats': seats})

# Booking View for user's to view their booking history
def BookingViewSet(request, movie, user):

    return render(request, 'bookings/booking_history.html', {'movie': movie})

# Movie View for CRUD operations on movies
def MovieViewSet(request):
    movies = Movie.objects.all()
    return render(request, 'bookings/movie_list.html', {"movies": movies})
    