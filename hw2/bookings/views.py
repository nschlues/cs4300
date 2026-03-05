from django.shortcuts import render, get_object_or_404
from .models import Movie, Seat, Booking 

def my_view(request):
    return render(request, 'my_page.html')

# Login View for user authentication
def LoginViewSet(request):
    return render(request, 'bookings/login.html')

# Signup View for new users
def RegisterViewSet(request):
    return render(request, 'bookings/register.html')

# Seat View for seat availability and booking
def SeatViewSet(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    seats = movie.seats.all()
    return render(request, 'bookings/seat_booking.html', {'movie': movie, 'seats': seats})

# Booking View for user's to view their booking history
def BookingViewSet(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'bookings/booking_history.html', {'bookings': bookings})

# Movie View for CRUD operations on movies
def MovieViewSet(request):
    movies = Movie.objects.all()
    return render(request, 'bookings/movie_list.html', {"movies": movies})
    