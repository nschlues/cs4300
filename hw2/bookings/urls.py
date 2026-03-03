from django.urls import path
from . import views

urlpatterns = [
    path("", views.BaseViewSet, name="base"),
    path("/api/movies", views.MovieViewSet , name="movies"),
    path("/api/seats", views.SeatViewSet , name="seats"),
    path("/api/bookings", views.BookingViewSet , name="bookings"),
]