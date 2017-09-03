# Created by leeha at 28/07/2017
#@get_ticket_ids
Feature: As a user without an account, I need to scan tickets at the venue (Negative Tests)

  Scenario:  Doorstaff without permission cannot scan tickets
    When I have logged in with Punter Email and Punter Password
    Then I am logged in


    When I am not a registered user
    When I scan a ticket id

  Scenario:  Doorstaff with permission for a single event do not have access to approve other events for that PVA

