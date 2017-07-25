import time

from pprint import pprint
from collections import namedtuple

from Config import Config
from ticketlab import UserPVA, UserPunter, StressTest


URL = Config.URL

PVAUSER = Config.PVAUSER
PVAPASSWORD = Config.PVAPASSWORD

EventDetails = namedtuple('EventDetails', 'name day month year hour minute price numTickets' #starthour startminute
                                              ' customField max_sell')


PUNTER1 = Config.PUNTER1
PUNTER1PASSWORD = Config.PUNTER1PASSWORD




###################################CREATE MULTIPLE EVENTS AND ADD TO A SERIES###########################################
#
# with UserPVA() as user:
#     #Log In
#     user.log_in(username=PVAUSER, password=PVAPASSWORD)
#
#     #Create Multiple Events
#     events = []
#     for event in range(10):
#         events.append(user.CreateNewEvent(EventDetails(name="StressTestEvent:{}".format(event+1), day="25", month="12", year="2018",
#                      hour="20", minute="30", price="0", numTickets="500",
#                      # starthour='20', startminute='30',
#                      customField='Tell me the name of your kid!',
#                      max_sell='500', )
#             )
#         )
#
#     print(events)
#
#     listofevents = [x for x,y in events]
#
#     #Create a New Series
#     x = user.CreateSeries("Test Series", listofevents)
#
#     print("Series id:" + x)
#
#     #Log Out
#     user.log_out()
#
#

#######################################BUY MULTIPLE TICKETS FOR A SERIES################################################
#
# with UserPunter() as punter:
#     #Log In
#     punter.log_in(username=PUNTER1, password=PUNTER1PASSWORD)
#
#
#     #get all event ids from a series id
#     ##Nice to have for now!!
#
#     listofevents = [388,] #, 384, 385, 386, 387, 388] #382-391 383-388 = empty still
#     total_tickets = 500
#     groups_of = 1
#
#     #Bulk Buy Tickets
#     listoftickets = punter._bulk_buy_tickets(listofevents, total_tickets, groups_of)
#     print(listoftickets) #list of ticket id's
#
#     #Log Out
#     punter.log_out()
#
#
############################################RUN STRESS TEST#############################################################

listofevents = [382, 383, 384, 385, 386, 387, 388, 389, 390, 391]

listoftickets = []

# Get Ticket IDs for Events
with UserPVA() as user:
    # Log In
    user.log_in(username=PVAUSER, password=PVAPASSWORD)
    for event in listofevents:
        print("Getting ticket ids for {}".format(str(event)))
        listoftickets = listoftickets + user.get_tickets(event)
    #Log Out
    user.log_out()

listofticket_ids = [d['ticket_id'] for d in listoftickets]


with StressTest() as test:
    #Event 382
    #dummy_ticket_list = ['382fnqh', '382dggn', '382duru', '382dbsi', '382xsir','382fnqh', '382dggn', '382duru', '382dbsi', '382xsir','382fnqh', '382dggn', '382duru', '382dbsi', '382xsir']
    #listofticket_ids = dummy_ticket_list



    #Buy all the tickets!
    print("Testing", len(listofticket_ids), "tickets...... pls wait")
    time.sleep(5)
    x = test.run(listofticket_ids) # add a second param of how many tickets to dupe scan (random from listofticket_ids list)
    print("\n")
    print("-----------------")
    count = sum(list(x[1].values()))
    print(str(count), "results returned")
    print("-----------------")
    print("Response Messages")
    print(x[0])
    print("-----------------")
    print("Status Codes")
    print(x[1])
    print("\n")


