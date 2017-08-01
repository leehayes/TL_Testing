import TL_Testing.TicketLab.ticketlab as tl
from TL_Testing.TicketLab.Config import Config


def before_all(context):
    context.events = []


def after_all(context):
    pass


def before_feature(context, feature):
    if 'Login_PVA' in feature.tags:
        # context.excute_steps('''
        context.browser = tl.UserPVA()
        context.browser.__enter__()
        context.browser.log_in(Config.PVAUSER, Config.PVAPASSWORD)
