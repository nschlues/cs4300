Feature: Movie Listing

    Scenario: A visitor views the movie list
        Given there are 3 movies in the database
        When I visit the movies page
        Then I should see 3 movies listed

    Scenario: A visitor clicks on a movie to view its seats
        Given there is a movie called "The Matrix"
        When I visit the movies page
        Then I should see a link to book seats for "The Matrix"