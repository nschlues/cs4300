from django.urls import path
from . import views

urlpatterns = [
    #path("", views.BaseViewSet, name="base"),
    path("", views.MovieViewSet , name="movies"),
    path("bookings/", views.BookingViewSet , name="bookings"),
    path("book/<int:movie_id>/", views.SeatViewSet, name="book_seat"),
    path("login/", views.LoginViewSet, name="login"),
    path("signup/", views.RegisterViewSet, name="register"),
]