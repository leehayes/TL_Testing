import asyncio
import time

import aiohttp
import async_timeout
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select

from TL_Testing.TicketLab.Config import Config
URL = Config.URL
MY_DIR = Config.MY_DIR
OS = Config.OS

class BrowserInstance:
    '''
    The base class which manages the Selenium instance and provides time logging.
    Set up as context manager
    '''

    def __init__(self, base_url=URL, proxy=None, username=None, password=None):
        '''
        :param base_url: The home URL, defaults to the test environment
        :param proxy: Defaults to None, important to use when testing with multiple requests
        '''

        self.base_url = base_url
        self.proxy = proxy
        self.username = username
        self.password = password


    def __enter__(self):
        '''
        Set up Selenium and Timer
        :return: self
        '''
        self.start = time.time()
        # Choose correct chromedriver
        if OS == "Win":
            self.chromedriver = r"{}TL_Testing/TicketLab/driver/chromedriver".format(MY_DIR)
        else:
            self.chromedriver = r"{}TL_Testing/TicketLab/driver/chromedriverMac".format(MY_DIR)

            #FF
            #binary = FirefoxBinary('TL_Testing/TicketLab/driver/geckodriver')
            #self.driver = webdriver.Firefox(firefox_binary=binary)
            #self.firefoxdriver = r"{}TL_Testing/TicketLab/driver/geckodriver".format(MY_DIR)
            #self.driver = webdriver.Firefox()

        self.driver = webdriver.Chrome(self.chromedriver)
        # driver.set_window_position(-10000, 0)
        self.driver.set_page_load_timeout(30)
        self.driver.get(self.base_url)
        return self

    def __exit__(self, *args):
        '''
        Close Selenium browser and calculate time taken
        *args will accept the following 3 parameters:
        :param exc_type: Error Handling
        :param exc_val: Error Handling
        :param exc_tb: Error Handling
        :return: None
        '''
        #time.sleep(10000)
        self.driver.quit()
        end = time.time()
        print('Browser closed : {} seconds'.format(int(end - self.start)))

    def log_in(self, username, password):
        self.driver.get(self.base_url+"/login")

        self.username = username
        self.password = password
        details_dict = {"email": self.username,
                        "password": self.password,}

        for k, v in details_dict.items():
            Xpath = "// input[ @ name = '" + k + "']"
            x = self.driver.find_element_by_xpath(Xpath)
            x.send_keys(v)

        Xpath = "// input[ @ type = 'submit']"
        button = self.driver.find_element_by_xpath(Xpath)
        button.click()

    def log_out(self, ):
        self.driver.get(self.base_url+"/login/logout")

    def _click_button(self, text, times=1):
        ''' Clicks a button that matches the text
        :param text: Str of button text to find
        :param times: number of times to click the button (default = once)
        :return: None
        '''

        button = self.driver.find_element_by_xpath('//button[contains(text(), "{}")]'.format(text))
        for click in range(times):
            button.click()
        return None

    def buy_tickets(self, event_id, no_of_tickets=1):
        ''' Buy tickets without being logged in (will be expected to provide email and password
        :param event_id: int of event id - converted to str
        :param no_of_tickets: (int) Number of tickets to buy - defaults to 1
        :return: int(ticket id)
        '''

        event_id = str(event_id)
        no_of_tickets = no_of_tickets

        # Go to the buy tickets page
        self.driver.get(self.base_url + "/buy/id/{}".format(event_id))

        # increase tickets
        self._click_button("+", times=no_of_tickets - 1)

        buttons = self.driver.find_elements_by_css_selector('.button')
        buttons[0].click()

        # Page refreshed to recalc cost of tickets. Get buttons again and submit form
        buttons = self.driver.find_elements_by_css_selector('.button')
        buttons[1].click()

        # Submit
        Xpath = "// input[ @ type = 'submit']"
        button = self.driver.find_element_by_xpath(Xpath)
        button.click()

    def enter_user_random_details(self, email, first_name, surname):

        # Populate forename
        Xpath = "// input[ @ name = 'forename']"
        elem = self.driver.find_element_by_xpath(Xpath)
        elem.send_keys(first_name)

        # Populate surname
        Xpath = "// input[ @ name = 'surname']"
        elem = self.driver.find_element_by_xpath(Xpath)
        elem.send_keys(surname)

        # Populate telephone no
        Xpath = "// input[ @ name = 'telephone']"
        elem = self.driver.find_element_by_xpath(Xpath)
        elem.send_keys("01689824686")

        # Populate email
        Xpath = "// input[ @ name = 'email']"
        elem = self.driver.find_element_by_xpath(Xpath)
        elem.send_keys(email)

        # Populate custom field
        Xpath = "// input[ @ name = 'customField']"
        elem = self.driver.find_element_by_xpath(Xpath)
        elem.send_keys("Testing customField")

        # Populate password
        Xpath = "// input[ @ name = 'password']"
        elem = self.driver.find_element_by_xpath(Xpath)
        elem.send_keys("password")
        Xpath = "// input[ @ name = 'confirm']"
        elem = self.driver.find_element_by_xpath(Xpath)
        elem.send_keys("password")

        # Details page. Untick email options
        checkbox_dict = {"ticketlab_optin": False,
                         "promoter_optin": False, }
        for k, v in checkbox_dict.items():
            Xpath = "// input[ @ name = '" + k + "']"
            x = self.driver.find_element_by_xpath(Xpath)
            x.click()  # click on the checkbox to deselect

        # Submit
        Xpath = "// input[ @ type = 'submit']"
        button = self.driver.find_element_by_xpath(Xpath)
        button.click()

        # Get Ticket ID
        Ticket_id = None
        Xpath = "// img[contains(@src, '{}/images/qrs/')]".format(self.base_url)
        img = self.driver.find_element_by_xpath(Xpath)

    @property
    def text(self):
        return self.driver.page_source

    @property
    def url(self):
        return self.driver.current_url

    def go_to_url(self, url):
        self.driver.get(self.base_url + url)


class UserPunter(BrowserInstance):
    '''
    A user instance to buy tickets
    '''

    def __init__(self):
        super(UserPunter, self).__init__()

    def _bulk_buy_tickets(self, event_list, total_tickets, groups_of):
        ''' Loops through the events and buys tickets in groups. Built primarily for
        stress testing purposes
        :param event_list: List of event ids
        :param total_tickets: Number of tickets in events (assumes all the same)
        :param groups_of: The group number for each ticket (must be a multiple of total_tickets)
        :return: List of ticket ids
        '''

        qr_codes = int(total_tickets / groups_of)

        # Buy Tickets
        # loop through series of events and buy all the tickets in batches of 2
        ticket_id_list = []

        for event in event_list:
            for purchase in range(qr_codes):
                print("Event : {} : {} out of {} tickets".format(str(event), str(purchase + 1), str(qr_codes),))
                try:
                    x = self.buy_tickets(event, groups_of)
                    ticket_id_list.append(x)
                except:
                    print("Unable to create ticket. Will try again")
        return ticket_id_list


    def buy_tickets(self, event_id, no_of_tickets = 1):
        ''' Buy tickets
        :param event_id: int of event id - converted to str
        :param no_of_tickets: (int) Number of tickets to buy - defaults to 1
        :return: int(ticket id)
        '''

        event_id = str(event_id)
        no_of_tickets = no_of_tickets

        #Go to the buy tickets page
        self.driver.get(self.base_url + "/buy/id/{}".format(event_id))

        #increase tickets
        self._click_button("+", times=no_of_tickets-1)

        buttons = self.driver.find_elements_by_css_selector('.button')
        buttons[0].click()

        #Page refreshed to recalc cost of tickets. Get buttons again and submit form
        buttons = self.driver.find_elements_by_css_selector('.button')
        buttons[1].click()

        #Populate custom field
        Xpath = "// input[ @ name = 'customField']"
        elem = self.driver.find_element_by_xpath(Xpath)
        elem.send_keys("Testing customField")

        #Details page. Untick email options
        checkbox_dict = {"ticketlab_optin": False,
                        "promoter_optin": False,}
        for k, v in checkbox_dict.items():
            Xpath = "// input[ @ name = '" + k + "']"
            x = self.driver.find_element_by_xpath(Xpath)
            x.click() # click on the checkbox to deselect

        #Submit
        Xpath = "// input[ @ type = 'submit']"
        button = self.driver.find_element_by_xpath(Xpath)
        button.click()

        #Get Ticket ID
        Ticket_id = None
        Xpath = "// img[contains(@src, '{}/images/qrs/')]".format(self.base_url)
        img = self.driver.find_element_by_xpath(Xpath)

        #return ticket id
        return img.get_attribute("src").split("/")[-1].split(".")[0]

    def create_new_event(self, eventdetails):
        ''' Set Up a New Event
        :param eventdetails: A namedtuple containing all event details necessary for set up
        :return: Event ID and Name as a tuple
        '''

        eventdetails = eventdetails

        self.driver.get(self.base_url + "/add/event")

        # UPDATE INPUTS
        # Name
        Xpath = "// input[@name = 'name']"
        input = self.driver.find_element_by_xpath(Xpath)
        input.send_keys(eventdetails.name)

        # Day Month Year
        select = Select(self.driver.find_element_by_xpath("//select[@name='day']"))
        select.select_by_value(eventdetails.day)
        select = Select(self.driver.find_element_by_xpath("//select[@name='month']"))
        select.select_by_value(eventdetails.month)
        select = Select(self.driver.find_element_by_xpath("//select[@name='year']"))
        select.select_by_value(eventdetails.year)

        # Time (hack)
        # tab after year to get hour, the tab again to get minute
        elem = self.driver.find_element_by_name("year")
        elem.send_keys(Keys.TAB, eventdetails.hour)  # tab over to hour, which is a not-visible element
        elem.send_keys(Keys.TAB * 2, eventdetails.minute)  # tab over to minute, which is a not-visible element

        # price
        Xpath = "// input[@name = 'price']"
        input = self.driver.find_element_by_xpath(Xpath)
        input.send_keys(eventdetails.price)

        # numTickets
        Xpath = "// input[@name = 'numTickets']"
        input = self.driver.find_element_by_xpath(Xpath)
        input.send_keys(eventdetails.numTickets)

        # #starthour
        # Xpath = "// input[@name = 'starthour']"
        # input = self.driver.find_element_by_xpath(Xpath)
        # input.send_keys(eventdetails.starthour)
        #
        # #startminute
        # Xpath = "// input[@name = 'startminute']"
        # input = self.driver.find_element_by_xpath(Xpath)
        # input.send_keys(eventdetails.startminute)

        # customField
        Xpath = "// input[@name = 'customField']"
        input = self.driver.find_element_by_xpath(Xpath)
        input.send_keys(eventdetails.customField)

        # max_sell
        Xpath = "// input[@name = 'max_sell']"
        input = self.driver.find_element_by_xpath(Xpath)
        input.send_keys(eventdetails.max_sell)

        # Populate Description and T&Cs
        elem = self.driver.find_element_by_name("specifySaleStart")
        elem.send_keys(Keys.TAB, "It's gonna be fun")  # tab over to description, which is a not-visible element
        elem = self.driver.find_element_by_name("specifySaleStart")
        elem.send_keys(Keys.TAB * 2, "NO REFUNDS \n You break it, you bought it")  # tab over to terms

        # Submit
        Xpath = "// input[ @ type = 'submit']"
        button = self.driver.find_element_by_xpath(Xpath)
        button.click()

        # return event id and event name
        return self.driver.current_url.split("/")[-1], eventdetails.name


class UserPVA(BrowserInstance):
    '''
    A Promoter, Venue or Artist user instance to buy tickets and/or view tickets available
    '''
    def __init__(self):
        super(UserPVA, self).__init__()

    def add_venue(self, event_dict=None):
        '''
        Populates Base URL /add/venue . This page opens when "Add venue" option selected
        This is also used when creating first event
        :param event_dict: defaults to None and takes the default event dict below
        :return: None
        '''

        self.driver.get(self.base_url+"/add/venue")

        # Add a venue
        event_dict = event_dict
        if event_dict is None:
            event_dict = {"venue_name": "The Pub",
                          "capacity": "1000",
                          "address1": "Hoe Street",
                          "address2": "Walthamstow",
                          "town": "London",
                          "postcode": "E17 9LG"}

        Xpath = "// input[@type = 'text']"
        fieldsets = self.driver.find_elements_by_xpath(Xpath)
        for i in fieldsets:
            i.send_keys(event_dict[i.get_attribute('name')])

        Xpath = "// input[@type='submit']"
        button = self.driver.find_element_by_xpath(Xpath)
        button.click()

    def create_new_event(self, eventdetails):
        ''' Set Up a New Event
        :param eventdetails: A namedtuple containing all event details necessary for set up
        :return: Event ID and Name as a tuple
        '''

        eventdetails = eventdetails

        self.driver.get(self.base_url + "/add/event")

        #UPDATE INPUTS

        #Name
        Xpath = "// input[@name = 'name']"
        input = self.driver.find_element_by_xpath(Xpath)
        input.send_keys(eventdetails.name)

        #Day Month Year
        select = Select(self.driver.find_element_by_xpath("//select[@name='day']"))
        select.select_by_value(eventdetails.day)
        select = Select(self.driver.find_element_by_xpath("//select[@name='month']"))
        select.select_by_value(eventdetails.month)
        select = Select(self.driver.find_element_by_xpath("//select[@name='year']"))
        select.select_by_value(eventdetails.year)

        #Time (hack)
        #tab after year to get hour, the tab again to get minute
        elem = self.driver.find_element_by_name("year")
        elem.send_keys(Keys.TAB, eventdetails.hour)  # tab over to hour, which is a not-visible element
        elem.send_keys(Keys.TAB*2, eventdetails.minute)  # tab over to minute, which is a not-visible element

        #price
        Xpath = "// input[@name = 'price']"
        input = self.driver.find_element_by_xpath(Xpath)
        input.send_keys(eventdetails.price)

        #numTickets
        Xpath = "// input[@name = 'numTickets']"
        input = self.driver.find_element_by_xpath(Xpath)
        input.send_keys(eventdetails.numTickets)

        # #starthour
        # Xpath = "// input[@name = 'starthour']"
        # input = self.driver.find_element_by_xpath(Xpath)
        # input.send_keys(eventdetails.starthour)
        #
        # #startminute
        # Xpath = "// input[@name = 'startminute']"
        # input = self.driver.find_element_by_xpath(Xpath)
        # input.send_keys(eventdetails.startminute)

        #customField
        Xpath = "// input[@name = 'customField']"
        input = self.driver.find_element_by_xpath(Xpath)
        input.send_keys(eventdetails.customField)

        #max_sell
        Xpath = "// input[@name = 'max_sell']"
        input = self.driver.find_element_by_xpath(Xpath)
        input.send_keys(eventdetails.max_sell)

        #Populate Description and T&Cs
        elem = self.driver.find_element_by_name("specifySaleStart")
        elem.send_keys(Keys.TAB, "It's gonna be fun")  # tab over to description, which is a not-visible element
        elem = self.driver.find_element_by_name("specifySaleStart")
        elem.send_keys(Keys.TAB*2, "NO REFUNDS \n You break it, you bought it")  # tab over to terms

        #Submit
        Xpath = "// input[ @ type = 'submit']"
        button = self.driver.find_element_by_xpath(Xpath)
        button.click()

        #return event id and event name
        return self.driver.current_url.split("/")[-1], eventdetails.name

    def edit_event(self, event_id, eventdetails):
        ''' Edit an Event
        :
        :param event_id: id of event to edit
        :param eventdetails: A dict or keyword args containing all event details to amend
        :return: None
        '''
        self.driver.get(self.base_url + "/index.php/add/event/" + str(event_id))

        for k, v in eventdetails.items():
            Field = k
            Value = v

        # UPDATE INPUTS

        if Field == "name":
            Xpath = "// input[@name = 'name']"
            input = self.driver.find_element_by_xpath(Xpath)
            input.send_keys(30 * Keys.BACKSPACE)
            input.send_keys(Value)

        elif Field == "day":
            select = Select(self.driver.find_element_by_xpath("//select[@name='day']"))
            select.select_by_value(Value)
        elif Field == "month":
            select = Select(self.driver.find_element_by_xpath("//select[@name='month']"))
            select.select_by_value(Value)
        elif Field == "year":
            select = Select(self.driver.find_element_by_xpath("//select[@name='year']"))
            select.select_by_value(Value)
        elif Field == "hour":
            elem = self.driver.find_element_by_name("year")
            elem.send_keys(Keys.TAB, Value)  # tab over to hour, which is a not-visible element
        elif Field == "minute":
            elem = self.driver.find_element_by_name("year")
            elem.send_keys(Keys.TAB * 2, Value)  # tab over to minute, which is a not-visible element
        elif Field == "price":
            Xpath = "// input[@name = 'price']"
            input = self.driver.find_element_by_xpath(Xpath)
            input.send_keys(10 * Keys.BACKSPACE)
            input.send_keys(Value)
        elif Field == "opt_in_out":
            Xpath = "// input[ @ name = 'private']"
            x = self.driver.find_element_by_xpath(Xpath)
            x.click()  # click on the checkbox to deselect
        elif Field == "password_protect":
            Xpath = "// input[ @ name = 'passwordProtect']"
            x = self.driver.find_element_by_xpath(Xpath)
            x.click()  # click on the checkbox to select


        # Submit
        Xpath = "// input[ @ type = 'submit']"
        button = self.driver.find_element_by_xpath(Xpath)
        button.click()

    def toggle_event_off_and_on_sale(self, event_id):
        self.driver.get(self.base_url + "/index.php/admin/toggle_live/" + str(event_id))

    def event_is_off_sale(self, event_id):
        self.driver.get(self.base_url + "/index.php/event/id/" + str(event_id))
        http = self.driver.page_source
        return ("Not on sale" in http)

    def clone_event(self, event_id):
        self.driver.get(self.base_url + "/index.php/add/event/" + str(event_id) + "/clone")
        # Submit
        Xpath = "// input[ @ type = 'submit']"
        button = self.driver.find_element_by_xpath(Xpath)
        button.click()


    def check_event_details(self, event_id):
        '''
        :param event_id: id for the event
        :return: http text for the event page
        '''
        self.driver.get(self.base_url + "/index.php/event/id/" + str(event_id))
        http = self.driver.page_source
        return http

    def get_live_events(self, single_row=None):
        '''
        Gets all live events for the PVA
        :return: a list of events, each event represented by a dict
        '''

        list_of_live_events = []

        self.driver.get(self.base_url + "/index.php/dashboard")
        Xpath = "// div[@class = 'TableWrapper']"
        tables = self.driver.find_elements_by_xpath(Xpath)
        Xpath = "// tr[ *]"
        table = tables[0].find_elements_by_xpath(Xpath)

        while len(table[0].text) == 0:  # make sure all cells are populated
            # print("Table not yet populated, sleeping......")
            time.sleep(2)

        table = table[1:-1]  # trim headers and footer

        table_length = (len(table))
        if single_row == "single_row":
            table_length = 1

        for row in range(table_length):  # bug when looping through table - Use len counter instead
            try:
                cells = table[row].find_elements_by_tag_name("td")
                links = table[row].find_elements_by_tag_name("a")
                event_id = links[0].get_attribute('href').split("/")[-1]
                list_of_live_events.append({"name": cells[0].text,
                                            "event_id": event_id,
                                            "date_time": cells[1].text,
                                            "venue": cells[2].text, })
            except:
                pass

        return list_of_live_events

    def create_series(self, seriesname="New Series", eventlist=None):
        '''
        Create a Series out of a list of created events
        :param seriesname: Str name of the series
        :param eventlist: List of str event ids
        :return: Tuple of str Series ID and Name
        '''
        self.driver.get(self.base_url + "/add/series")
        eventlist = eventlist

        #Series Name
        Xpath = "// input[@name = 'name']"
        input = self.driver.find_element_by_xpath(Xpath)
        input.send_keys(seriesname)

        #Select Events to Add to Series
        Xpath = "// input[@type = 'checkbox']"
        checkboxes = self.driver.find_elements_by_xpath(Xpath)
        for checkbox in checkboxes:
            if checkbox.get_attribute('value') in eventlist:
                checkbox.click()

        #Submit
        Xpath = "// input[ @ type = 'submit']"
        button = self.driver.find_element_by_xpath(Xpath)
        button.click()

        return self.driver.current_url.split("/")[-1], seriesname

    def get_tickets(self, eventid):
        self.driver.get(self.base_url + "/index.php/event/allocation/{}".format(str(eventid)))
        eventid = eventid

        Xpath = "// tr[ *]"
        table = self.driver.find_elements_by_xpath(Xpath)
        table = table[2:-1] #trim headers and footer
        table_length = len(table)
        listoftickets = []

        while len(table[0].text) == 0: #make sure all cells are populated
            #print("Table not yet populated, sleeping......")
            time.sleep(2)

        for row in range(table_length): # bug when looping through table - Use len counter instead
                cells = table[row].find_elements_by_tag_name("td")
                try:
                    listoftickets.append({"ticket_id": cells[4].text,
                                          "event_id": str(eventid),
                                          "no_of_tickets": cells[3].text,
                                          "user": cells[2].text,
                                          })
                except:
                    #In the event of some tickets being "Already admitted", skip the header and continue
                    #collecting ticket ids
                    pass

        return listoftickets

    def get_cookies(self):
        cookies = self.driver.get_cookies()
        return cookies

    @staticmethod
    async def scan_ticket(session, url):
        '''
        Replicates the process of sending a http request when scanning in a ticket
        :param session:
        :param url: url for ticket confirmation
        :return: tuple responce code (200 = ok) followed by accept/reject string
        '''
        with async_timeout.timeout(30):
            async with session.get(url) as response:
                text = await response.text()
                status = response.status
                if "has not started yet" in text:
                    msg = "NOT_STARTED"
                elif "Valid ticket" in text:
                    msg = "VALID"
                elif "This ticket has already been claimed." in text:
                    msg = "DUPLICATE"
                elif "You need to sign in to be able to acknowledge ticket codes" in text:
                    msg = "NOT_LOGGED_IN"
                else:
                    msg = "ERROR"

        return status, msg

    def buy_tickets(self, event_id, no_of_tickets=1):
        ''' Buy tickets
        :param event_id: int of event id - converted to str
        :param no_of_tickets: (int) Number of tickets to buy - defaults to 1
        :return: int(ticket id)
        '''

        event_id = str(event_id)
        no_of_tickets = no_of_tickets

        # Go to the buy tickets page
        self.driver.get(self.base_url + "/buy/id/{}".format(event_id))

        # increase tickets
        self._click_button("+", times=no_of_tickets - 1)

        buttons = self.driver.find_elements_by_css_selector('.button')
        buttons[0].click()

        # Page refreshed to recalc cost of tickets. Get buttons again and submit form
        buttons = self.driver.find_elements_by_css_selector('.button')
        buttons[1].click()

        # Populate custom field
        Xpath = "// input[ @ name = 'customField']"
        elem = self.driver.find_element_by_xpath(Xpath)
        elem.send_keys("Testing customField")

        # Details page. Untick email options
        checkbox_dict = {"ticketlab_optin": False,
                         "promoter_optin": False, }
        for k, v in checkbox_dict.items():
            Xpath = "// input[ @ name = '" + k + "']"
            x = self.driver.find_element_by_xpath(Xpath)
            x.click()  # click on the checkbox to deselect

        # Submit
        Xpath = "// input[ @ type = 'submit']"
        button = self.driver.find_element_by_xpath(Xpath)
        button.click()

        # Get Ticket ID
        Ticket_id = None
        Xpath = "// img[contains(@src, '{}/images/qrs/')]".format(self.base_url)
        img = self.driver.find_element_by_xpath(Xpath)

        # return ticket id
        return img.get_attribute("src").split("/")[-1].split(".")[0]



class StressTest():
    '''
    This context manager will generate concurrent http post messages
    to replicate scanning a large number of tickets
    '''

    def __init__(self,):
        pass

    def __enter__(self):
        '''
        Set up Timer
        :return: self
        '''
        self.start = time.time()

        return self

    def __exit__(self, *args):
        '''
        On completion of responses, calculate time taken
        *args will accept the following 3 parameters:
        :param exc_type: Error Handling
        :param exc_val: Error Handling
        :param exc_tb: Error Handling
        :return: None
        '''

        end = time.time()
        print('Responses all received : {} seconds'.format(int(end - self.start)))

    def run(self, listofticket_ids):
        '''
        This is the concurrent method which will call mulitple HTTP requests for a list of tickets and dupes.
        :param listofticket_ids:
        :return: Dict - Returns 2 dicts of count of different responses and status codes
        '''
        loop = asyncio.get_event_loop()

        q = asyncio.Queue()
        for ticket in listofticket_ids:
            q.put_nowait(ticket)

        async def worker(work_queue):
            worker_results = []
            try:
                async with aiohttp.ClientSession() as session:
                    #login to get session cookie
                    login_data = {'redirect': 'login', 'email': Config.PVAUSER, 'password': Config.PVAPASSWORD,}
                    r = await session.post(Config.URL+'/index.php/login/login_action', data=login_data)
                    while not work_queue.empty():
                        queue_item = await work_queue.get()
                        worker_result = await UserPVA.scan_ticket(session, Config.URL+"/ticket/"+queue_item)
                        worker_results.append(worker_result)
            except:
                print("Error on worker thread - Closing worker")
                return worker_results
            return  worker_results
        #8 scanners
        tasks = []
        for i in range(8):
            tasks.append(asyncio.ensure_future(worker(q)))

        completed_results = loop.run_until_complete(asyncio.gather(*tasks))
        loop.close()

        results = []
        for result in completed_results:
            results = results + result


        results_dict = {}
        status_dict = {}
        for result in results:
            results_dict[result[1]] = results_dict.get(result[1], 0) + 1
            status_dict[result[0]] = status_dict.get(result[0], 0) + 1

        return results_dict, status_dict


