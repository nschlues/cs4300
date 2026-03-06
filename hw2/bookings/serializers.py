from rest_framework import serializers
from .models import Seat, Movie, Booking

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        seat = Seat
        fields = '__all__'
        
# Do not include the user field for privacy. Just show all combined bookings
class BookingSerializer(serializers.ModelSerializer):
    class Meta: 
        booking = Booking
        fields = ['movie', 'seat', 'is_booked']

