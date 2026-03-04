from django.apps import AppConfig


class BookingsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bookings'

    def ready(self):
        from django.db.models.signals import post_migrate
        from django.core.management import call_command

def load_seed(sender, **kwargs):
    from bookings.models import Movie, Seat, Booking
    if not Movie.objects.exists():  
        call_command('loaddata', 'fixtures/movies.json')
    if not Seat.objects.exists():  
        call_command('loaddata', 'fixtures/seats.json')
    if not Booking.objects.exists():  
        call_command('loaddata', 'fixtures/bookings.json')

        post_migrate.connect(load_seed, sender=self)