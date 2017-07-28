## Created by leehayes at 25/07/2017

Feature: PVA users can manage their events (Negative Tests)
  As a Promoter, Venue or Artist I wish to be able to set up, view and edit my events

  Scenario: Punter cannot create a new event
    Given I click the logout button
    Given I have logged in with Punter Email and Password Punter Password
    Then I'll see Punter Username on the page

    #Create EVENT as user by going to the create event url

    Given I click the logout button
    Given I have logged in with PVA Email and Password PVA Password
    Then I'll see PVA Username on the page


  Scenario: PVA cannot edit another user's event
    # Enter steps here


  Scenario: PVA cannot view the dashboard of another PVA user
    # Enter steps here

#  Scenario: Send an email to those attending the event
#    # Enter steps here
#
#
#  Scenario: Set up an even where ticket sales don't start until a later date
#    # Enter steps here
#
#  Scenario: Set up new event
#    # Enter steps here
#
#
#  Scenario: Set up new event
#    # Enter steps here