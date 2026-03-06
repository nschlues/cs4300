import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movie_theater_booking.settings')
django.setup()

from django.test import Client
from django.test.utils import setup_test_environment

def before_all(context):
    setup_test_environment()

def before_scenario(context, scenario):
    context.client = Client()

def after_scenario(context, scenario):
    from bookings.models import Movie, Seat, Booking
    from django.contrib.auth.models import User
    Booking.objects.all().delete()
    Seat.objects.all().delete()
    Movie.objects.all().delete()
    User.objects.all().delete()