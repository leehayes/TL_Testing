from datetime import datetime, timedelta
from collections import namedtuple
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


def before_all(context):
    context.events = []


def after_all(context):
    pass


def before_feature(context, feature):
    if 'Login_PVA' in feature.tags:
        context.browser = tl.UserPVA()
        context.browser.__enter__()
        context.browser.log_in(Config.PVAUSER, Config.PVAPASSWORD)
    if 'Get_Events' in feature.tags:
        context.browser = tl.UserPVA()
        context.browser.__enter__()
        context.browser.log_in(Config.PVAUSER, Config.PVAPASSWORD)

        cost = str(0)
        no_of_events = 2
        event_date = datetime.now() + timedelta(hours=1)

        day = str(event_date.day)
        month = str(event_date.month)
        year = str(event_date.year)
        hour = str(event_date.hour)
        minute = str(event_date.minute)

        EventDetails = namedtuple('EventDetails',
                                  'name day month year hour minute price numTickets'  # starthour startminute
                                  ' customField max_sell')

        context.events = []
        ticket_id_list = []

        for event in range(no_of_events):
            event_id, event_name = context.browser.create_new_event(
                EventDetails(name="BDD_Scanning_Test:{}".format(str(event + 1)),
                             day=day, month=month, year=year,
                             hour=hour, minute=minute, price=cost, numTickets="100",
                             # starthour='20', startminute='30',
                             customField='This is a scan test',
                             max_sell='100', )
            )

            context.events.append(event_id)
            # context.browser.go_to_url("/buy/id/" + str(event_id))
            x = context.browser.buy_tickets(event_id, 2)
            ticket_id_list.append(x)

        print(context.events)
        print(ticket_id_list)
