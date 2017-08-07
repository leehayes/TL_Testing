# Created by leeha at 04/08/2017
Feature: As a user, I need to be able to book tickets
  # It must be possible to log in with an account, or as a new user, registering for the first time

  Scenario: As a PVA User, I can buy tickets for my own event
    Given I have logged in with PVA Email and Password PVA Password
    Given I have selected an event to buy
    Then I select the event and choose to buy 2 tickets

  Scenario: As a Punter User, I can buy tickets for a PVA user's event
    Given I have logged in with PVA Email and Password PVA Password
    Given I have selected an event to buy
    Given I click the logout button
    Given I have logged in with Punter Email and Password Punter Password
    Then I select the event and choose to buy 2 tickets

  Scenario: As an unregistered User, I can buy tickets for a PVA user's event
    Given I have logged in with PVA Email and Password PVA Password
    Given I have selected an event to buy
    Given I click the logout button
    Given I am not a registered user
    Then I go to the event and select 2 tickets
    Then I enter my details, using a random email
    Then I choose to buy 2 tickets

  Scenario: Password protected event
