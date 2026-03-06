Feature: Seat Availability

    Scenario: A visitor views seats for a movie
        Given there is a movie called "Inception"
        When I visit the seat booking page for "Inception"
        Then I should see 15 seats

    Scenario: A visitor sees which seats are booked
        Given there is a movie called "Inception"
        And seat "A1" for "Inception" is already booked
        When I visit the seat booking page for "Inception"
        Then seat "A1" should be marked as "Booked"
        And seat "A2" should be marked as "Open"

    Scenario: A visitor views a non-existent movie
        When I visit the seat booking page for movie id 9999
        Then I should get a 404 response