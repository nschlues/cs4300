Feature: Seat Booking

    Scenario: A logged in user books an available seat
        Given I am logged in as "test" with password "test"
        And there is a movie called "The Matrix"
        And seat "A1" for "The Matrix" is available
        When I book seat "A1" for "The Matrix"
        Then seat "A1" should be marked as booked
        And the booking should appear in my booking history

    Scenario: A logged out user cannot book a seat
        Given there is a movie called "The Matrix"
        And I am not logged in
        When I visit the booking history page
        Then I should be redirected to the login page

    Scenario: A user cannot book an already booked seat
        Given I am logged in as "test" with password "test"
        And there is a movie called "The Matrix"
        And seat "A1" for "The Matrix" is already booked
        When I book seat "A1" for "The Matrix"
        Then no new booking should be created

    Scenario: A user only sees their own bookings
        Given I am logged in as "test" with password "test"
        And "otheruser" has a booking for "The Matrix"
        When I visit the booking history page
        Then I should not see "otheruser"'s bookings