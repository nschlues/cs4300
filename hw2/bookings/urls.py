from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'movies', MovieViewSet)
router.register(r'seats', SeatViewSet)
router.register(r'bookings', BookingViewSet)

urlpatterns = [
    # User Interface URLs
    path("", views.MovieViewSet , name="movies"),
    path("bookings/", views.BookingViewSet , name="bookings"),
    path("book/<int:movie_id>/", views.SeatViewSet, name="book_seat"),
    path("login/", views.LoginView, name="login"),
    path("signup/", views.SignUpView, name="register"),
    path("logout/", views.LogoutView, name="logout"),

    # API URLs
    path('api/', include(router,urls)),
]