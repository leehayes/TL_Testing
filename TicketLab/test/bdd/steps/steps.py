from behave import *

import TL_Testing.TicketLab.ticketlab as tl
from TL_Testing.TicketLab.Config import Config


@given('I have logged in with a {user_email} and Password {user_password}')
def step_open_browser_and_login(context, user_email, user_password):
    emails = {"PVA Email": Config.PVAUSER,
              "Punter Email": Config.PUNTER1,
              }
    passwords = {"PVA Password": Config.PVAPASSWORD,
                 "Punter Password": Config.PUNTER1PASSWORD,
                 }

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
        username = Config.PVANAME
    elif username == "Punter Username":
        username = Config.PUNTER1NAME
    assert (username in context.browser.text) is True


@when("I'll see {username} on the page")
def step_do_this_and_that(context, username):
    pass


@then("I'll get a message saying it happened")
def step_get_a_msg(context, ):
    pass
