from django.urls import path
from . import views

urlpatterns = [
    # User Interface URLs
    path("", views.MovieViewSet , name="movies"),
    path("bookings/", views.BookingViewSet , name="bookings"),
    path("book/<int:movie_id>/", views.SeatViewSet, name="book_seat"),
    path("login/", views.LoginView, name="login"),
    path("signup/", views.SignUpView, name="register"),

    # API URLs
    
]