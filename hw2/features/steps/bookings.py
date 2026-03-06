from behave import given, when, then
from django.urls import reverse
from django.contrib.auth.models import User
from bookings.models import Movie, Seat, Booking
from datetime import date


@given('"otheruser" has a booking for "{title}"')
def step_other_user_booking(context, title):
    other_user, _ = User.objects.get_or_create(
        username='otheruser',
        defaults={'password': 'pass1234'}
    )
    movie = Movie.objects.get(title=title)
    # Use last seat so it doesn't conflict with other scenarios
    seat = movie.seats.filter(is_booked=False).last()
    seat.is_booked = True
    seat.save()
    Booking.objects.create(user=other_user, movie=movie, seat=seat)


@when('I book seat "{seat_number}" for "{title}"')
def step_book_seat(context, seat_number, title):
    movie = Movie.objects.get(title=title)
    seat = Seat.objects.get(movie=movie, seat_number=seat_number)
    context.response = context.client.post(
        reverse('bookings'),
        {'seat_id': seat.id, 'movie_id': movie.id},
        follow=True
    )


@when('I visit the booking history page')
def step_visit_bookings(context):
    context.response = context.client.get(reverse('bookings'), follow=True)


@then('seat "{seat_number}" should be marked as booked')
def step_seat_is_booked(context, seat_number):
    # Find the movie from context if available, otherwise get from DB
    movie = getattr(context, 'movie', Movie.objects.last())
    seat = Seat.objects.get(movie=movie, seat_number=seat_number)
    seat.refresh_from_db()
    assert seat.is_booked, f'Expected seat {seat_number} to be booked but it was not'


@then('the booking should appear in my booking history')
def step_booking_in_history(context):
    context.response = context.client.get(reverse('bookings'))
    assert context.response.status_code == 200
    assert len(context.response.context['bookings']) > 0, \
        'Expected at least one booking in history but found none'


@then('no new booking should be created')
def step_no_booking_created(context):
    # Only bookings that existed before the attempt should be present
    user = User.objects.get(username='testuser')
    bookings = Booking.objects.filter(user=user)
    assert bookings.count() == 0, \
        f'Expected 0 bookings but found {bookings.count()}'


@then("I should not see \"otheruser\"'s bookings")
def step_no_other_bookings(context):
    assert context.response.status_code == 200
    bookings = context.response.context['bookings']
    for booking in bookings:
        assert booking.user.username != 'otheruser', \
            "Found otheruser's booking in current user's history"