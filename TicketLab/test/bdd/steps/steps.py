from collections import namedtuple
from datetime import datetime, timedelta

from behave import *
from dateutil.relativedelta import relativedelta

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


@then("I'll get a message saying it happened")
def step_get_a_msg(context, ):
    pass


@when("I enter and submit {no_of_events} new {cost} event in {time_unit} {time_measure} time")
def step_create_event(context, no_of_events, cost, time_unit, time_measure):
    if cost == "free":
        cost = 0
    else:
        cost = float(cost)

    if no_of_events == "a":
        no_of_events = 0
    else:
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
    pass

    for event in range(no_of_events):
        event_id, event_name = context.browser.CreateNewEvent(
            EventDetails(name="BDD_Test_Event:{}".format(str(event + 1)),
                         day="25", month="12", year="2017",
                         hour="20", minute="30", price="0", numTickets="500",
                         # starthour='20', startminute='30',
                         customField='Tell me the name of your kid!',
                         max_sell='500', )
            )
