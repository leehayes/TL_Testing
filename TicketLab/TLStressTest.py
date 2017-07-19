from Config import Config
from ticketlab import UserPVA, UserPunter
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

with UserPunter() as punter:
    #Log In
    punter.log_in(username=PUNTER1, password=PUNTER1PASSWORD)

    #get all event ids from a series id (this method could be needed by PVA or Punter class
    #Nice to have for now!!

    #Buy Tickets
    #loop through series of events and buy all the tickets in batches of 2
    x = punter.buy_tickets(382, 2)
    print("ticket code returned by Buy Tickets : " + x)

    #Log Out
    #punter.log_out()


