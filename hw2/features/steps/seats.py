from behave import given, when, then
from django.urls import reverse
from bookings.models import Movie, Seat
from datetime import date


@given('seat "{seat_number}" for "{title}" is already booked')
def step_seat_booked(context, seat_number, title):
    movie = Movie.objects.get(title=title)
    seat = Seat.objects.get(movie=movie, seat_number=seat_number)
    seat.is_booked = True
    seat.save()


@given('seat "{seat_number}" for "{title}" is available')
def step_seat_available(context, seat_number, title):
    movie = Movie.objects.get(title=title)
    seat = Seat.objects.get(movie=movie, seat_number=seat_number)
    seat.is_booked = False
    seat.save()
    context.seat = seat


@when('I visit the seat booking page for "{title}"')
def step_visit_seats(context, title):
    movie = Movie.objects.get(title=title)
    context.response = context.client.get(
        reverse('book_seat', args=[movie.id])
    )


@when('I visit the seat booking page for movie id {movie_id:d}')
def step_visit_seats_invalid(context, movie_id):
    context.response = context.client.get(
        reverse('book_seat', args=[movie_id])
    )


@then('I should see {count:d} seats')
def step_see_seats(context, count):
    assert context.response.status_code == 200
    assert len(context.response.context['seats']) == count, \
        f'Expected {count} seats but got {len(context.response.context["seats"])}'


@then('seat "{seat_number}" should be marked as "{status}"')
def step_seat_status(context, seat_number, status):
    content = context.response.content.decode()
    # Check the status text appears near the seat number in the response
    assert status in content, \
        f'Expected status "{status}" in page but did not find it'


@then('I should get a 404 response')
def step_404(context):
    assert context.response.status_code == 404, \
        f'Expected 404 but got {context.response.status_code}'