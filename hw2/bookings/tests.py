from django.test import TestCase
from django.contrib.auth.models import User
from .models import Movie, Seat, Booking 
from datetime import date 


class MovieModelTest(TestCase):
    def setUp(self):
        self.movie = Movie.objects.create(
            title = 'Test Movie',
            description = 'This is a test movie',
            release_date = date(2025, 12, 20),
            duration = 120,
        )

    def test_movie_create(self):
        self.assertEqual(str(self.movie), "Test Movie")
        self.assertEqual(str(self.movie.description), "This is a test movie")

    def test_seats_generated(self):
        self.assertEqual(self.movie.seats.count(), 15)

    def test_correct_seats(self):
        seat_nums = list(self.movie.seats.values_list("seat_num", flat=True))
        expected_nums = [f"{row}{i}" for row in ["A", "B", "C"] for i in range(1, 6)]
        self.assertEqual(seat_nums, expected_nums)

    def test_seats_start_unbooked(self):
        self.assertFalse(self.movie.seats.filter(is_booked=True).exists)


class SeatModelTest(TestCase):
    def setUp(self):
        self.movie = Seat.objects.create(
            movie = 'Seat Test Movie',
            description="desc",
            release_date=date(2024, 1, 1),
            duration=90,
        )
        self.seat = self.movie.seats.first()

    def test_seat_string(self):
        self.assertIn("Seat Test Movie", str(self.seat))
        self.assertIn(self.seat.seat_number, str(self.seat))
        self.assertFalse(self.seat.is_booked)

    def test_seat_num(self):
        self.assertEqual(str(self.seat.seat_number), "A1")

    def test_can_be_booked(self):
        self.seat.is_booked = True
        self.seat.save()
        self.seat.refresh_from_db()
        self.assertTrue(self.seat.is_booked)


class BookingModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test", password="test")
        self.movie = Movie.objects.create(
            title="Test Booking Movie",
            description="desc",
            release_date=date(2024, 1, 1),
            duration=100,
        )
        self.seat = self.movie.seats.first()

    def test_create_booking(self):
        booking = Booking.objects.create(
            user=self.user, movie=self.movie, seat=self.seat
        )
        self.assertEqual(booking.user, self.user)
        self.assertEqual(booking.movie, self.movie)
        self.assertEqual(booking.seat, self.seat)


    def test_booking_exists(self):
        booking = Booking.objects.create(
            user=self.user, movie=self.movie, seat=self.seat
        )
        self.assertIn("testuser", str(booking))



class LoginViewTest(TestCase):





class SignUpViewTest(TestCase):



class LogoutViewTest(TestCase):



class RegisterViewSetTest(TestCase):



class SeatViewSetTest(TestCase):




class BookingViewSetTest(TestCase):




class MovieViewSetTest(TestCase):