import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select


class BrowserInstance:
    '''
    The base class which manages the Selenium instance and provides time logging.
    Set up as context manager
    '''

    def __init__(self, base_url="http://aphasian.com/ticketlab", proxy=None, username=None, password=None):
        '''
        :param base_url: The home URL, defaults to the aphasian test environment
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
        self.chromedriver = r"/Users/leeha/mycode/driver/chromedriver"
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
        time.sleep(10000)
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


class UserPunter(BrowserInstance):
    '''
    A user instance to buy tickets and/or view tickets available
    '''
    def __init__(self):
        super(UserPunter, self).__init__()

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

    def buy_tickets(self, event_id, no_of_tickets = 1):
        ''' Buy tickets
        Precondition: User session must be logged in as a non-PVA
        :param eventid: Event id of ticket purchase
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

        # # Submit
        # Xpath = "// input[ @ type = 'submit']"
        # button = self.driver.find_element_by_xpath(Xpath)
        # button.click()

        #return event id and event name
        return self.driver.current_url.split("/")[-1]



class UserPVA(BrowserInstance):
    '''
    A Promoter, Venue or Artist user instance to buy tickets and/or view tickets available
    '''
    def __init__(self):
        super(UserPVA, self).__init__()

    def CreateNewEvent(self, eventdetails):
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

    def CreateSeries(self, seriesname="New Series", eventlist = None):
        '''
        Create a Series out of a list of created events
        :param seriesname: Str name of the series
        :param eventlist: List of str event ids
        :return: Tuple of str Series ID and Name
        '''
        self.driver.get(self.base_url + "/add/series")
        self.eventlist = eventlist

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




