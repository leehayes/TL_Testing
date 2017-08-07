# Created by leeha at 04/08/2017
Feature: As a user, I need to be able to book tickets (Negative Tests)

  Scenario: As an unregistered User, I can't buy tickets using an already registered email
    Given I have logged in with PVA Email and Password PVA Password
    When I enter and submit a new free event in 1 hour time
    Then I'll see my event with ID
    Given I have selected an event to buy
    Given I click the logout button
    Given I am not a registered user
    Then I go to the event and select 2 tickets
    Then I enter the details with Punter Email email address

