from behave import *


def before_all(context):
    print("starting up")
    pass
    # context.browser = Browser()


def after_all(context):
    print("clost")
    pass
    # context.browser.close()


@given('I have logged in as a {user}')
def step_open_browser_and_login(context, user):
    if user == "PVA User":
        # login as a PVA User
        # Confirm logged in
        pass
    pass


@when('I do this and that')
def step_do_this_and_that(context, ):
    pass


@then("I'll get a message saying it happened")
def step_get_a_msg(context, ):
    pass
