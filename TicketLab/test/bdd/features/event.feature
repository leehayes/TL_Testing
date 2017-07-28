# Created by leehayes at 27/07/2017
@Login_PVA
Feature: PVA users can manage their events
  As a Promoter, Venue or Artist I wish to be able to set up, view and edit my events

  Scenario: Set up new event
    When I enter and submit a new free event(s) in 1 hours time
    Then I'll see my event(s) with an ID


  Scenario: Create 2 events and create a series
    When I enter and submit 2 new free event(s) in 1 hours time
    Then I'll see my event(s) with an ID


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
#  Scenario: Add new venue
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