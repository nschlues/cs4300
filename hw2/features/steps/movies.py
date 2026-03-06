from behave import given, when, then
from django.urls import reverse
from bookings.models import Movie
from datetime import date


@given('there are {count:d} movies in the database')
def step_create_movies(context, count):
    for i in range(count):
        Movie.objects.create(
            title=f'Test Movie {i}',
            description='A test movie description',
            release_date=date(2024, 1, 1),
            duration=120,
        )


@given('there is a movie called "{title}"')
def step_create_movie(context, title):
    context.movie = Movie.objects.get_or_create(
        title=title,
        defaults={
            'description': 'A test movie description',
            'release_date': date(2024, 1, 1),
            'duration': 120,
        }
    )[0]


@when('I visit the movies page')
def step_visit_movies(context):
    context.response = context.client.get(reverse('movies'))


@then('I should see {count:d} movies listed')
def step_see_movies(context, count):
    assert context.response.status_code == 200
    assert len(context.response.context['movies']) == count, \
        f'Expected {count} movies but got {len(context.response.context["movies"])}'


@then('I should see a link to book seats for "{title}"')
def step_see_movie_link(context, title):
    assert title in context.response.content.decode(), \
        f'Expected to find "{title}" in the page but did not'