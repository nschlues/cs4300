from django.db import models
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Movie Model
class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    release_date = models.DateField()
    duration = models.IntegerField(help_text="Duration in minutes")

    def __str__(self):
        return self.title


# Seat Model
class Seat(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='seats', null=True, blank=True)
    seat_number = models.CharField(max_length=10)
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.movie.title} - Seat {self.seat_number}"


# Booking Model
class Booking(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.movie} - {self.seat}"

# Create Seats for Movies when they are created
@receiver(post_save, sender=Movie)
def create_seats_for_movie(sender, instance, created, **kwargs):
    if created:
        seats = [
            Seat(movie=instance, seat_number=f"{row}{i}")
            for row in ['A', 'B', 'C']
            for i in range(1, 6)
        ]
        Seat.objects.bulk_create(seats)