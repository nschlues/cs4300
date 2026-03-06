from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Movie, Seat, Booking
from datetime import date
from rest_framework.test import APIClient
from rest_framework import status

## Unit tests
# Model tests
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
        seat_nums = list(self.movie.seats.values_list("seat_number", flat=True))
        expected_nums = [f"{row}{i}" for row in ["A", "B", "C"] for i in range(1, 6)]
        self.assertEqual(seat_nums, expected_nums)

    def test_seats_start_unbooked(self):
        self.assertFalse(self.movie.seats.filter(is_booked=True).exists())


class SeatModelTest(TestCase):
    def setUp(self):
        self.movie = Movie.objects.create(
            title = 'Seat Test Movie',
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
        self.assertIn("test", str(booking))


# View Tests
class LoginViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="test", password="test")

    def test_page_load(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)

    def test_valid_login(self):
        response = self.client.post(
            reverse("login"), {"username": "test", "password": "test"}
        )
        self.assertRedirects(response, reverse("movies"))

    def test_invalid_pass(self):
        response = self.client.post(
            reverse("login"), {"username": "test", "password": "wrongpass"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid username or password")

    def test_invlaid_username(self):
        response = self.client.post(
            reverse("login"), {"username": "nobody", "password": "test"}
        )
        self.assertContains(response, "Invalid username or password")    




class SignUpViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_page_load(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)

    def test_user_creation(self):
        response = self.client.post(
            reverse("register"), {"username": "newuser", "password": "newpass"}
        )
        self.assertRedirects(response, reverse("movies"))
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_login_new_user(self):
        self.client.post(
            reverse("register"), {"username": "newuser", "password": "newpass"}
        )
        response = self.client.get(reverse("movies"))
        self.assertContains(response, "Logout")

    def test_duplicate_username(self):
        User.objects.create_user(username="existing", password="pass1234")
        response = self.client.post(
            reverse("register"), {"username": "existing", "password": "newpass123"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "An error occurred")



class LogoutViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="test", password="test")

    def test_page_load(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)

    def test_logout_clears_session(self):
        self.client.login(username="test", password="test")
        self.client.post(reverse("logout"))
        response = self.client.get(reverse("bookings"))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('bookings')}")



class SeatViewSetTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.movie = Movie.objects.create(
            title="Seat View Movie",
            description="desc",
            release_date=date(2024, 1, 1),
            duration=95,
        )

    def test_seat_page_loads(self):
        response = self.client.get(reverse("book_seat", args=[self.movie.id]))
        self.assertEqual(response.status_code, 200)

    def test_seat_page_shows_movie_title(self):
        response = self.client.get(reverse("book_seat", args=[self.movie.id]))
        self.assertContains(response, "Seat View Movie")

    def test_seat_page_shows_all_seats(self):
        response = self.client.get(reverse("book_seat", args=[self.movie.id]))
        self.assertEqual(len(response.context["seats"]), 15)

    def test_seat_page_invalid_movie(self):
        response = self.client.get(reverse("book_seat", args=[9999]))
        self.assertEqual(response.status_code, 404)


class BookingViewSetTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="test", password="test")
        self.movie = Movie.objects.create(
            title="Bookable Movie",
            description="desc",
            release_date=date(2024, 1, 1),
            duration=120,
        )
        self.seat = self.movie.seats.first()

    def test_booking_history_requires_login(self):
        response = self.client.get(reverse("bookings"))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('bookings')}")

    def test_booking_history_loads(self):
        self.client.login(username="test", password="test")
        response = self.client.get(reverse("bookings"))
        self.assertEqual(response.status_code, 200)

    def test_create_booking_marks_seat_booked(self):
        self.client.login(username="test", password="test")
        self.client.post(
            reverse("bookings"), {"seat_id": self.seat.id, "movie_id": self.movie.id}
        )
        self.seat.refresh_from_db()
        self.assertTrue(self.seat.is_booked)

    def test_create_booking_saved_to_db(self):
        self.client.login(username="test", password="test")
        self.client.post(
            reverse("bookings"), {"seat_id": self.seat.id, "movie_id": self.movie.id}
        )
        self.assertEqual(Booking.objects.filter(user=self.user).count(), 1)

    def test_cannot_double_book_seat(self):
        self.seat.is_booked = True
        self.seat.save()
        self.client.login(username="test", password="test")
        self.client.post(
            reverse("bookings"), {"seat_id": self.seat.id, "movie_id": self.movie.id}
        )
        self.assertEqual(Booking.objects.count(), 0)

    def test_booking_history_shows_own_bookings(self):
        Booking.objects.create(user=self.user, movie=self.movie, seat=self.seat)
        self.client.login(username="test", password="test")
        response = self.client.get(reverse("bookings"))
        self.assertContains(response, "Bookable Movie")

    def test_booking_history_excludes_other_users(self):
        other_user = User.objects.create_user(username="othertest", password="test")
        other_seat = self.movie.seats.last()
        Booking.objects.create(user=other_user, movie=self.movie, seat=other_seat)
        self.client.login(username="test", password="test")
        response = self.client.get(reverse("bookings"))
        self.assertEqual(len(response.context["bookings"]), 0)



class MovieViewSetTest(TestCase):
    def setUp(self):
        self.client = Client()
        Movie.objects.create(
            title="Listed Movie",
            description="desc",
            release_date=date(2024, 1, 1),
            duration=110,
        )

    def test_movie_list_loads(self):
        response = self.client.get(reverse("movies"))
        self.assertEqual(response.status_code, 200)

    def test_movie_list_shows_movies(self):
        response = self.client.get(reverse("movies"))
        self.assertContains(response, "Listed Movie")

    def test_movie_list_accessible_without_login(self):
        response = self.client.get(reverse("movies"))
        self.assertEqual(response.status_code, 200)

## Integration tests
class MovieAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.movie = Movie.objects.create(
            title="test movie",
            description="desc",
            release_date=date(1999, 3, 31),
            duration=136,
        )

    def test_get_movies_returns_200(self):
        response = self.client.get('/api/movies/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_movies_returns_list(self):
        response = self.client.get('/api/movies/')
        self.assertEqual(len(response.data), 1)

    def test_movie_has_expected_fields(self):
        response = self.client.get('/api/movies/')
        movie = response.data[0]
        self.assertIn('title', movie)
        self.assertIn('description', movie)
        self.assertIn('release_date', movie)
        self.assertIn('duration', movie)

    def test_movie_fields_have_correct_values(self):
        response = self.client.get('/api/movies/')
        movie = response.data[0]
        self.assertEqual(movie['title'], 'test movie')
        self.assertEqual(movie['duration'], 136)

    def test_post_creates_movie(self):
        data = {
            'title': 'test movie 2',
            'description': 'desc',
            'release_date': '2010-07-16',
            'duration': 148,
        }
        response = self.client.post('/api/movies/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Movie.objects.count(), 2)

    def test_post_returns_created_movie_data(self):
        data = {
            'title': 'test movie 2',
            'description': 'desc',
            'release_date': '2010-07-16',
            'duration': 148,
        }
        response = self.client.post('/api/movies/', data, format='json')
        self.assertEqual(response.data['title'], 'test movie 2')

    def test_delete_movie_returns_204(self):
        response = self.client.delete(f'/api/movies/{self.movie.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_movie_removes_from_db(self):
        self.client.delete(f'/api/movies/{self.movie.id}/')
        self.assertEqual(Movie.objects.count(), 0)


class SeatAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.movie1 = Movie.objects.create(
            title="test movie",
            description="desc",
            release_date=date(1999, 3, 31),
            duration=136,
        )
        self.movie2 = Movie.objects.create(
            title="test movie 2",
            description="desc",
            release_date=date(2010, 7, 16),
            duration=148,
        )

    def test_get_all_seats_returns_200(self):
        response = self.client.get('/api/seats/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_seats_by_movie_returns_correct_count(self):
        response = self.client.get(f'/api/seats/?movie={self.movie1.id}')
        self.assertEqual(len(response.data), 15)

    def test_filter_seats_by_movie_returns_only_that_movies_seats(self):
        response = self.client.get(f'/api/seats/?movie={self.movie1.id}')
        for seat in response.data:
            self.assertEqual(seat['movie'], self.movie1.id)

    def test_filter_seats_excludes_other_movies(self):
        response = self.client.get(f'/api/seats/?movie={self.movie1.id}')
        movie_ids = [seat['movie'] for seat in response.data]
        self.assertNotIn(self.movie2.id, movie_ids)

    def test_all_seats_start_unbooked(self):
        response = self.client.get(f'/api/seats/?movie={self.movie1.id}')
        for seat in response.data:
            self.assertFalse(seat['is_booked'])

    def test_all_seats_match_movie_count(self):
        response = self.client.get('/api/seats/')
        movie_count = Movie.objects.count()
        expected_seats = movie_count * 15
        self.assertEqual(len(response.data), expected_seats)


class BookingAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="test", password="test")
        self.other_user = User.objects.create_user(username="otheruser", password="pass")
        self.movie = Movie.objects.create(
            title="test movie",
            description="desc",
            release_date=date(1999, 3, 31),
            duration=136,
        )
        self.seat = self.movie.seats.first()

    def test_get_bookings_without_login_returns_401_or_403(self):
        response = self.client.get('/api/bookings/')
        self.assertIn(response.status_code, [
            status.HTTP_401_UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN
        ])

    def test_get_bookings_with_login_returns_200(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/bookings/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_bookings_only_returns_current_users_bookings(self):
        # Create a booking for the current user
        Booking.objects.create(user=self.user, movie=self.movie, seat=self.seat)
        # Create a booking for another user
        other_seat = self.movie.seats.last()
        Booking.objects.create(user=self.other_user, movie=self.movie, seat=other_seat)

        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/bookings/')

        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['user'], self.user.id)

    def test_post_booking_without_login_returns_401_or_403(self):
        response = self.client.post(
            '/api/bookings/',
            {'movie': self.movie.id, 'seat': self.seat.id},
            format='json'
        )
        self.assertIn(response.status_code, [
            status.HTTP_401_UNAUTHORIZED,
            status.HTTP_403_FORBIDDEN
        ])

    def test_post_booking_creates_booking(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            '/api/bookings/',
            {'movie': self.movie.id, 'seat': self.seat.id},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.count(), 1)

    def test_post_booking_marks_seat_as_booked(self):
        self.client.force_authenticate(user=self.user)
        self.client.post(
            '/api/bookings/',
            {'movie': self.movie.id, 'seat': self.seat.id},
            format='json'
        )
        self.seat.refresh_from_db()
        self.assertTrue(self.seat.is_booked)

    def test_post_booking_sets_user_automatically(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            '/api/bookings/',
            {'movie': self.movie.id, 'seat': self.seat.id},
            format='json'
        )
        self.assertEqual(response.data['user'], self.user.id)

    def test_cannot_book_already_booked_seat(self):
        self.seat.is_booked = True
        self.seat.save()
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            '/api/bookings/',
            {'movie': self.movie.id, 'seat': self.seat.id},
            format='json'
        )
        # Should not create a booking
        self.assertEqual(Booking.objects.count(), 0)
        self.assertNotEqual(response.status_code, status.HTTP_201_CREATED)