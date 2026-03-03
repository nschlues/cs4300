from django.urls import path
from . import views

urlpatterns = [
    path("", views.BaseViewSet, name="base"),
    path("movies/", views.MovieViewSet , name="movies"),
    path("seats/", views.SeatViewSet , name="seats"),
    path("bookings/", views.BookingViewSet , name="bookings"),
    path("book/<int:movie_id>/", views.SeatViewSet, name="book_seat"),
]