# Created by leehayes at 27/07/2017
Feature: Users can log in and out
  As a PVA or Punter I wish to be able to log in

  Scenario: Log in and out as a PVA user
    Given I have logged in with PVA Email and Password PVA Password
    Then I'll see PVA Username on the page
    Given I click the logout button
    Then I am logged out

  Scenario: Log in and out as a Punter user
    Given I have logged in with Punter Email and Password Punter Password
    Then I'll see Punter Username on the page
    Given I click the logout button
    Then I am logged out
