# Created by leehayes at 27/07/2017
@Login_PVA
Feature: PVA users can manage their events
  As a Promoter, Venue or Artist I wish to be able to set up, view and edit my events

  Scenario: Set up new event
    When I enter and submit a new free event in 1 hour time
    Then I'll see my event with ID

  Scenario Outline: Edit an existing event
    Given I have selected an event to edit
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
    Given I have selected an event to edit
    When I take the event off sale
    Then the event page shows the event as Not on sale
    When I list the event as on sale
    Then the event page shows the event as On sale

  Scenario: I can clone an event
    Given I have selected an event to edit
    When I select the option to clone.
    Then I get a new event id

  Scenario: I can create an opt-out event
    Given I have selected an event to edit
    When I edit the event field name, to Opt-Out Event Test
    Given I have selected an event to edit
    When I edit the event field opt_in_out, to click_box
    When I go to the public event page
    Then There will be no event called Opt-Out Event Test publicly visible
    And The event is still visible via the buy ticket url

  Scenario: Password protected events are not visible on the main screen
    Given I have selected an event to edit
    When I edit the event field name, to Password Protected Event
    Given I have selected an event to edit
    When I edit the event field password_protect, to click_box
    When I go to the public event page
    Then There will be no event called Password Protected Event publicly visible
    And The event is still visible via the buy ticket url

  Scenario: As a Punter user I can set up my own events
    Given I click the logout button
    Then I am logged out
    Given I have logged in with Punter Email and Password Punter Password
    When I enter and submit a new free event in 1 hour time
    Then I'll see my event with ID