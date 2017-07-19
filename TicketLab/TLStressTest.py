from Config import Config
from ticketlab import UserPVA, UserPunter, StressTest
from collections import namedtuple


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

#series ID = 6
#http://aphasian.com/ticketlab/series/id/6
#
with UserPunter() as punter:
    #Log In
    punter.log_in(username=PUNTER1, password=PUNTER1PASSWORD)


    #get all event ids from a series id
    ##Nice to have for now!!

    events = [388,]#, 388, 389, 390, 391] #382-386
    total_tickets = 500
    groups_of = 5

    #Bulk Buy Tickets
    x = punter._bulk_buy_tickets(events, total_tickets, groups_of)
    print(x) #list of ticket id's

    #Log Out
    punter.log_out()


############################################RUN STRESS TEST#############################################################
#
# with StressTest() as test:
#
#     test.run()
