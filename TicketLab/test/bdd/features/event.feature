# Created by leehayes at 27/07/2017
Feature: PVA users can manage their events
  As a Promoter, Venue or Artist I wish to be able to set up, view and edit my events

  Scenario: Set up new event
#THIS FIRST STEP SHOULD BE IN ENVIRONMENT before_event.
    Given I have logged in with a PVA Email and Password PVA Password
    When I go to the event creation page
    Then I'll see PVA Username on the page



#
#  Scenario: Set up new event2
#    Given I have logged in as a PVA User
#    When I do this and that
#    Then I'll get a message saying it happened
#

#
#  Scenario Outline: User logs in
#      Given a user visits the site
#      When I log in as "<username>"
#      Then I should see the message <auth message>
#
#      Examples: Users
#        | username          | auth message               |
#        | registeredUser    | The meaning of life is 42  |
#        | unregisteredUser  | Please sign up             |

#
#  Scenario: Edit an existing event
#    Given something
#    When I do this and that
#    Then I'll get a message saying it happened
#
#
#  Scenario: View ticket sales for an event
#    Given I have logged in as a PVA User
#
#    # Enter steps here
#
#
#  Scenario: Add ticket sales sold manually for an event
#    # Enter steps here
#
#
#  Scenario: Send an email to those attending the event
#    # Enter steps here
#
#
#  Scenario: Set up an even where ticket sales don't start until a later date
#    # Enter steps here
#
#  Scenario: Set up new VENUE!!!
#    # Enter steps here
#
#
#  Scenario: Set up new event2
#    # Enter steps here