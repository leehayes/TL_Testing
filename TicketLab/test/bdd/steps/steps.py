from collections import namedtuple
from datetime import datetime, timedelta

from behave import *
from dateutil.relativedelta import relativedelta
from hamcrest import *

import TL_Testing.TicketLab.ticketlab as tl
from TL_Testing.TicketLab.Config import Config

emails = {"PVA Email": Config.PVAUSER,
          "Punter Email": Config.PUNTER1,
          }
passwords = {"PVA Password": Config.PVAPASSWORD,
             "Punter Password": Config.PUNTER1PASSWORD,
             }

usernames = {"PVA Username": Config.PVANAME,
             "Punter Username": Config.PUNTER1NAME,
             }


@given('I have logged in with {user_email} and Password {user_password}')
def step_open_browser_and_login(context, user_email, user_password):
    user_email = emails.get(user_email, user_email)
    user_password = passwords.get(user_password, user_password)
    if user_email == Config.PVAUSER:
        context.browser = tl.UserPVA()
    elif user_email == Config.PUNTER1:
        context.browser = tl.UserPunter()
    else:
        context.browser = tl.BrowserInstance()

    context.browser.__enter__()
    context.browser.log_in(user_email, user_password)


@then("I'll see {username} on the page")
def step_get_username(context, username):
    if username == "PVA Username":
        username = usernames.get(username)
    elif username == "Punter Username":
        username = usernames.get(username)
    else:
        username = username

    assert (username in context.browser.text) is True

@given("I click the logout button")
def step_logout(context, ):
    context.browser.log_out()

@then("I am logged out")
def step_confirm_logged_out(context, ):
    assert ("loginButton" in context.browser.text) is True


@when("I enter and submit a new {cost} event in {time_unit} {time_measure} time")
def step_create_single_event(context, cost, time_unit, time_measure):
    step_create_event(context, 1, cost, time_unit, time_measure)


@when("I enter and submit {no_of_events} new {cost} events in {time_unit} {time_measure} time")
def step_create_event(context, no_of_events, cost, time_unit, time_measure):
    if cost == "free":
        cost = 0
    else:
        cost = float(cost)

    no_of_events = int(no_of_events)


    if "day" in time_measure:
        event_date = datetime.now() + timedelta(days=int(time_unit))
    elif "month" in time_measure:
        event_date = datetime.now() + relativedelta(months=int(time_unit))
    elif "year" in time_measure:
        event_date = datetime.now() + relativedelta(years=int(time_unit))
    elif "hour" in time_measure:
        event_date = datetime.now() + timedelta(hours=int(time_unit))
    elif "minute" in time_measure:
        event_date = datetime.now() + timedelta(minutes=int(time_unit))
    else:
        event_date = datetime.now()

    day = str(event_date.day)
    month = str(event_date.month)
    year = str(event_date.year)
    hour = str(event_date.hour)
    minute = str(event_date.minute)

    EventDetails = namedtuple('EventDetails',
                              'name day month year hour minute price numTickets'  # starthour startminute
                              ' customField max_sell')

    context.events = []
    for event in range(no_of_events):
        event_id, event_name = context.browser.create_new_event(
            EventDetails(name="BDD_Test_Event:{}".format(str(event + 1)),
                         day=day, month=month, year=year,
                         hour=hour, minute=minute, price=cost, numTickets="100",
                         # starthour='20', startminute='30',
                         customField='Tell me the name of your kid!',
                         max_sell='100', )
            )
        context.events.append(event_id)


@then("I'll see my event with ID")
def step_single_event_id(context, ):
    step_event_id(context, )


@then("I'll see my events with IDs")
def step_event_id(context, ):
    no_of_events_created = len(context.events)
    assert_that(no_of_events_created, greater_than(0))


@when("I select the ids for my series called {series_name}")
def step_create_series(context, series_name):
    """
    :type context: behave.runner.Context
    """
    context.series = context.browser.create_series(seriesname=series_name, eventlist=context.events)
    context.events = []


@then("I'll see my series with ID")
def step_confirm_series_id(context):
    assert_that(len(context.series[0]), greater_than_or_equal_to(1))


@when("I edit the event field {field}, to {value}")
def step_edit_event(context, field, value, ):
    context.browser.edit_event(context.events[0], {field: value}, )


@then("the field {field}, will change on the events page to {value}")
def step_check_field(context, field, value, ):
    text = context.browser.check_event_details(context.events[0])
    assert_that((value in text), equal_to(True))


@given("I have selected an event to edit multiple times")
def step_get_event_to_edit(context):
    if not context.events:
        list_of_live_events = context.browser.get_live_events("single_row")
        for event in list_of_live_events:
            context.events.append(event.get("event_id"))
