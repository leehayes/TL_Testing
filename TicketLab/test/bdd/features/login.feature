# Created by leehayes at 27/07/2017
Feature: Users can log in and out
  As a PVA or Punter I wish to be able to log in

  Scenario Outline: Log in and out as a Punter or PVA user
    Given I have logged in with <Email> and Password <Password>
    Then I am logged in
    Then I'll see <Username> on the page
    Given I click the logout button
    Then I am logged out
    Examples:
      | Email        | Password        | Username        |
      | PVA Email    | PVA Password    | PVA Username    |
      | Punter Email | Punter Password | Punter Username |

