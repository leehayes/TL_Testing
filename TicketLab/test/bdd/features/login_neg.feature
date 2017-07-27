# Created by leehayes at 27/07/2017
Feature: Users can log in and out (Negative Tests)
  As a PVA or Punter I wish to be able to log in

  Scenario: Log in as a PVA user with wrong password
    Given I have logged in with a PVA Email and Password PVA Password
    Then I'll see wrongpassword on the page

  Scenario: Log in as a Punter user
    Given I have logged in with a Punter Email and Password Punter Password
    Then I'll see wrongpassword on the page
