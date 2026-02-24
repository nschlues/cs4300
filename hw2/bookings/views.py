from django.shortcuts import render, get_object_or_404
from .models import Movie 

# SeatViewSet
def SeatViewSet(request, ):


def BookingViewSet(request, movie, user):

    return render(request, 'book_seats.html', {'movie'})