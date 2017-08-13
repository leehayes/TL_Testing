# Created by leehayes at 28/07/2017
#@get_ticket_ids

#Preset up - Create 2 new events and return the ids.
@Get_Events
Feature: As a user without an account, I need to scan tickets at the venue

  Scenario: As a PVA User I want to set up door staff with permission to scan my tickets
    When I have logged in with PVA Email and Password PVA Password

  # Door staff will be scanning QR codes. The PVA user will provide them with a unique code which allows
  # the door staff to scan. The scanning process is replicated by calling the url directly, assuming the
  # QR code is correctly generated


  # Enter steps here

  #as door staff:

  #scan ticket




  Scenario:  A ticket cannot be scanned twice

  #view allocation list for event
  # view allocation list for PVAs event