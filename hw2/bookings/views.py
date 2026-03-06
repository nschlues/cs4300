from django.shortcuts import render, get_object_or_404, redirect
from .models import Movie, Seat, Booking 
from .forms import BookingForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import MovieSerializer, SeatSerializer, BookingSerializer


# Login View for user authentication
def LoginView(request):
    # Check if user is trying to login
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        # If they authenticated correctly
        if user is not None:
            user.last_login = timezone.now()
            user.save()
            login(request,user)
            return redirect('movies')
        # Error if the authentication was incorrect
        else:
            return render(request, 'bookings/login.html', {'error': 'Invalid username or password'})
    # User was directed to the page
    else: return render(request, 'bookings/login.html')

def SignUpView(request):
    # If user was submitting a signup request
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Try to create a user
        try:
            user = User.objects.create_user(username=username, password=password)
            user.save()
            login(request, user)
            return redirect('movies')
        # If registration failed provide error message
        except:
            return render(request, 'bookings/register.html', {'error': 'An error occurred. Please try again'})
    # Else render the page
    else:
        return render(request, 'bookings/register.html')

# Logout
def LogoutView(request):
    if request.method == 'POST':
        logout(request)
        return redirect('movies')

# Seat View for seat availability and booking
def SeatViewSet(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    seats = movie.seats.all()
    return render(request, 'bookings/seat_booking.html', {'movie': movie, 'seats': seats})

# Booking View for user's to view their booking history or to complete a booking
@login_required(login_url='login')
def BookingViewSet(request):
    if request.method == 'POST':
        seat_id = request.POST.get('seat_id')
        movie_id = request.POST.get('movie_id')

        seat = get_object_or_404(Seat, id=seat_id)
        movie = get_object_or_404(Movie, id=movie_id)

        # Prevent double-booking
        if seat.is_booked:
            return redirect('book_seat', movie_id=movie.id)

        # Create the booking
        Booking.objects.create(user=request.user, movie=movie, seat=seat)

        # Mark the seat as booked
        seat.is_booked = True
        seat.save()

        return redirect('bookings')

    # GET: show booking history
    else:
        bookings = Booking.objects.filter(user=request.user)
        return render(request, 'bookings/booking_history.html', {'bookings': bookings})

# Movie View for CRUD operations on movies
def MovieViewSet(request):
    movies = Movie.objects.all()
    return render(request, 'bookings/movie_list.html', {"movies": movies})


## API Views
class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    # Make users have to authenticate
    permission_classes = [IsAuthenticated]


class SeatViewSet(viewsets.ModelViewSet):
    queryset = Seat.objects.all()
    serializer_class = SeatSerializer

    # Only return seats for a specifif movie if provided
    def get_queryset(self):
        queryset = Seat.objects.all()
        movie_id = self.request.query_params.get(movie_id)
        if movie_id is not None:
            queryset = queryset.filter(movie_id)
        return queryset


class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = MovieSerializer
    # Make users have to authenticate
    permission_classes = [IsAuthenticated]

    # Requires user to be logged in to create bookings through the API
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # Makes user get only their bookings through the API
    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)
    
    queryset = Booking.objects.all()
