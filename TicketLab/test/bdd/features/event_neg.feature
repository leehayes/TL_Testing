## Created by leehayes at 25/07/2017

Feature: PVA users can manage their events (Negative Tests)
  As a Promoter, Venue or Artist I wish to be able to set up, view and edit my events

  Scenario: A user cannot edit another user's event
    Given I have logged in with PVA Email and Password PVA Password
    Given I have selected an event to edit
    Given I click the logout button
    Given I have logged in with Punter Email and Password Punter Password
    When I go to the edit event url
    Then I'll see Sorry, but it seems you're trying to edit an event that's not yours. Very naughty on the page


# Note - Unable to text if a user has access to another users dashboard and url is generic
  #http://aphasian.com/ticketlab/index.php/dashboard - Let me know if you think a QA test is necessary for this