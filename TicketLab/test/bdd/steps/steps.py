from collections import namedtuple
from datetime import datetime, timedelta
import random
import string
import time

from selenium.webdriver.common.keys import Keys
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


@then("I'll see {search_for_text} on the page")
def step_search_page_for_text(context, search_for_text):
    if search_for_text == "PVA Username":
        search_for_text = usernames.get(search_for_text)
    elif search_for_text == "Punter Username":
        search_for_text = usernames.get(search_for_text)
    else:
        search_for_text = search_for_text
    assert_that((search_for_text in context.browser.text), equal_to(True))

@given("I click the logout button")
def step_logout(context, ):
    context.browser.log_out()

@then("I am logged out")
def step_confirm_logged_out(context, ):
    assert_that(("loginButton" in context.browser.text), equal_to(True))
    assert_that(("logoutButton" in context.browser.text), equal_to(False))


@then("I am logged in")
def step_confirm_logged_out(context, ):
    assert_that(("loginButton" in context.browser.text), equal_to(False))
    assert_that(("logoutButton" in context.browser.text), equal_to(True))

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


@given("I have selected an event to edit")
def step_get_event_to_edit(context):
    if not context.events:
        list_of_live_events = context.browser.get_live_events("single_row")
        for event in list_of_live_events:
            context.events.append(event.get("event_id"))


@given("I have selected an event to buy")
def step_choose_an_event_to_buy(context):
    step_get_event_to_edit(context)


@given("I have a list of all my events")
def step_get_event_to_edit(context):
    if not context.events:
        list_of_live_events = context.browser.get_live_events()
        for event in list_of_live_events:
            context.events.append(event.get("event_id"))


@when("I take the event off sale")
def step_take_event_off_sale(context):
    context.browser.toggle_event_off_and_on_sale(context.events[0])


@then("the event page shows the event as Not on sale")
def step_check_event_not_on_sale(context):
    assert_that(context.browser.event_is_off_sale(context.events[0]), equal_to(True))


@when("I list the event as on sale")
def step_place_event_on_sale(context):
    context.browser.toggle_event_off_and_on_sale(context.events[0])

@then("the event page shows the event as On sale")
def step_check_event_not_on_sale(context):
    assert_that(context.browser.event_is_off_sale(context.events[0]), equal_to(False))

@when("I select the option to clone.")
def step_clone(context, ):
    context.browser.clone_event(context.events[0])

@then("I get a new event id")
def step_check_event_id_diff_to_context_event_id(context):
    assert_that(context.browser.url.split("/")[-1], not (equal_to(context.events[0])))

@when("I go to the edit event url")
def step_go_to_edit_event_url(context):
    context.browser.go_to_url("/index.php/add/event/" + str(context.events[0]))

@then("I select the event and choose to buy {no_of_tickets} tickets")
def step_buy_tickets(context, no_of_tickets):
    context.ticket_id = context.browser.buy_tickets(context.events[0], int(no_of_tickets))
    assert_that(len(context.ticket_id), greater_than_or_equal_to(7))

@given("I am not a registered user")
def step_change_context_browser_to_unregistered(context):
    """
    This replaces the previous PVA or Punter user session and replaces with a vanilla browser session
    """
    context.browser = tl.BrowserInstance()
    context.browser.__enter__()
    context.browser.username = "Randomy"
    context.browser.user_surname = "McRandomFace"

@then("I go to the event and select {no_of_tickets} tickets")
def step_select_tickets_and_submit(context, no_of_tickets):
    ticket_id = context.browser.buy_tickets(context.events[0], int(no_of_tickets))


@then("There will be no event called {event_name} publicly visible")
def step_opt_out_not_visible(context, event_name):
    time.sleep(200)
    text = context.browser.text
    context.browser.event_name = event_name
    assert_that((event_name in text), equal_to(False))


@when("I go to the public event page")
def step_go_to_public_events(context):
    context.browser.go_to_url("/index.php/tickets")


@step("The event is still visible via the buy ticket url")
def step_go_to_ticket_url(context):
    context.browser.go_to_url("/index.php/event/id/" + context.events[0])
    text = context.browser.text
    assert_that((context.browser.event_name in text), equal_to(True))
    context.browser.event_name = None


@then("I enter the details with {email} email address")
def step_enter_random_details(context, email):
    if email == "random":
        email = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
        email = 'delete-email-' + email + '@gmail.com'
    else:
        email = emails.get(email, email)
    context.browser.enter_user_random_details(email, context.browser.username, context.browser.user_surname)


@given("I go to the allocation list url")
def step_go_to_allocation_list_url(context):
    context.browser.go_to_url("/index.php/event/allocation/" + str(context.events[0]))


@given("I click the {button_text} button and enter {scanner_name}")
def step_click_a_button(context, scanner_name, button_text):
    context.scanner_name = scanner_name
    context.browser.go_to_url("/index.php/event/allocation/" + str(context.events[0]))
    context.browser._click_button(button_text)

    Xpath = "//input[@name='name']"
    elem = context.browser.driver.find_element_by_xpath(Xpath)
    elem.send_keys(scanner_name)
    elem.send_keys(Keys.TAB)
    elem.send_keys(Keys.ENTER)


@then("I get a verification id")
def step_get_verification_id(context):
    Xpath = "//p[*]"
    txt = context.browser.driver.find_elements_by_xpath(Xpath)
    print(txt[-1].text)
