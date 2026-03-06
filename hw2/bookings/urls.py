from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'movies', views.MovieViewSet)
router.register(r'seats', views.SeatViewSet)
router.register(r'bookings', views.BookingViewSet)

urlpatterns = [
    # User Interface URLs
    path("", views.movie_list_view, name="movies"),
    path("bookings/", views.booking_history_view, name="bookings"),
    path("book/<int:movie_id>/", views.seat_booking_view, name="book_seat"),
    path("login/", views.LoginView, name="login"),
    path("signup/", views.SignUpView, name="register"),
    path("logout/", views.LogoutView, name="logout"),

    # API URLs
    path('api/', include(router.urls)),
]