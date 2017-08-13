# Created by leehayes at 27/07/2017
Feature: Users can log in and out (Negative Tests)
  As a PVA or Punter I wish to be able to log in

  Scenario Outline: Log in as PVA user with wrong password
    Given I have logged in with <Email> and Password wrongpassword
    Then I'll see Invalid username or password on the page
    Examples:
      | Email        |
      | PVA Email    |
      | Punter Email |
