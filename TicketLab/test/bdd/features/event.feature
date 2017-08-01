# Created by leehayes at 27/07/2017
@Login_PVA
Feature: PVA users can manage their events
  As a Promoter, Venue or Artist I wish to be able to set up, view and edit my events

  Scenario: Set up new event
    When I enter and submit a new free event in 1 hour time
    Then I'll see my event with ID

  Scenario Outline: Edit an existing event
    Given I have selected an event to edit multiple times
    When I edit the event field <Field>, to <Value>
    Examples:
      | Field  | Value       |
      | name   | EDITED_NAME |
      | price  | 2020        |
      | day    | 20          |
      | month  | 10          |
      | year   | 2019        |
      | hour   | 20          |
      | minute | 20          |

    Then the field <Field>, will change on the events page to <Value>

  Scenario: Create 2 events and create a series
    When I enter and submit 2 new free events in 1 hours time
    Then I'll see my events with IDs
    When I select the ids for my series called Test_Series
    Then I'll see my series with ID

  Scenario: I can take tickets for an event off sale
    When I go to my dashboard
    And I take the top listed event off sale
    ##http://aphasian.com/ticketlab/index.php/admin/toggle_live/625
    Then The dashboard provides an option to put the event back on sale
    And the event page lists the event as Not on sale
    #http://aphasian.com/ticketlab/index.php/event/id/421

  Scenario: I can clone an event
  #http://aphasian.com/ticketlab/index.php/add/event/625/clone

