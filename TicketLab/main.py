import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select


'''
Bug when too many tickets ordered:
The number of tickets you have selected is more than we have! There % tickets left and n the queue though,
so if those orders aren't completed then those tickets will be re-released in 20 minutes or less.
'''


#Promoter, Venue or Artist (PVA)
#sign up
#log in
#create event
#create reccuring events
#create events with different tickets
#edit event
#cancel event

#punter
#search for tickets?

#select and buy tickets
#https://ticketlab.co.uk/buy/id/501
#What are the steps?
#Confirm no. of tickets - add and remove, order too many (sell out), check pricing calculates correctly
#Enter your details - Let it time out and try
#paypal (sandbox access for aphasian url or just select "FREE" gigs? id=304)
#confirm order and receive email (again, logic identifying aphasian url would help)


class BuyTickets:
    def __init__(self, url, ):
        self.url = url



    def click_button(self, text, times=1):

        ''' Clicks a button that matches the text

        :param text: Str of button text to find
        :param times: number of times to click the button (default = once)
        :return: None
        '''

        button = self.driver.find_element_by_xpath('//button[contains(text(), "{}")]'.format(text))
        for click in range(times):
            button.click()
        return None

    def __call__(self):
        """worker function"""
        start = time.time()

        self.chromedriver = r"/Users/leeha/mycode/driver/chromedriver"
        self.driver = webdriver.Chrome(self.chromedriver)
        # driver.set_window_position(-10000, 0)
        self.driver.set_page_load_timeout(30)

        self.driver.get(self.url)


        self.click_button("+", times=2)

        #self.driver.find_element_by_css_selector('.button').click()

        buttons = self.driver.find_elements_by_css_selector('.button')
        buttons[0].click()

        #Page refreshed to recalc cost of tickets. Get buttons again and submit form
        buttons = self.driver.find_elements_by_css_selector('.button')
        buttons[1].click()

        #Details page -  https://ticketlab.co.uk/buy/details

        details_dict = {"forename": "Lee",
                        "surname": "Hayes",
                        "email": "leehayes@gmail.com",
                        "telephone": "07888844065",
                        "customField": "Lewis",
                        "password": "mysupersecretpassword",
                        "confirm": "mysupersecretpassword",}

        for k, v in details_dict.items():
            Xpath = "// input[ @ name = '" + k + "']"
            x = self.driver.find_element_by_xpath(Xpath)
            x.send_keys(v)

        checkbox_dict = {"ticketlab_optin": False,
                        "promoter_optin": False,}
        for k, v in checkbox_dict.items():
            Xpath = "// input[ @ name = '" + k + "']"
            x = self.driver.find_element_by_xpath(Xpath)
            x.get_attribute('value')

            if v:
                if x.get_attribute('value') == "1" :
                    pass # True and already ticked
                else:
                    x.click() # click on the checkbox to select

            if not v:
                if x.get_attribute('value') == "0":
                    pass # False and already unticked
                else:
                    x.click() # click on the checkbox to deselect




        time.sleep(100000)
        self.driver.quit()

        end = time.time()
        print('Worker finished : {} seconds'.format(int(end - start)))


class CreateEvent:

    def __init__(self, url, username, password ):
        self.url = url
        self.username = username
        self.password = password

    def add_venue(self, ):
        '''
        Populates http://aphasian.com/ticketlab/add/venue
        Used when creating first event or "Add venue" option selected
        :return: None
        '''
        # Add a venue
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

    def __call__(self):
        """worker function"""
        start = time.time()

        self.chromedriver = r"/Users/leeha/mycode/driver/chromedriver"
        self.driver = webdriver.Chrome(self.chromedriver)
        # driver.set_window_position(-10000, 0)
        self.driver.set_page_load_timeout(30)

        self.driver.get(self.url)


        details_dict = {"email": self.username,
                        "password": self.password,}

        for k, v in details_dict.items():
            Xpath = "// input[ @ name = '" + k + "']"
            x = self.driver.find_element_by_xpath(Xpath)
            x.send_keys(v)

        Xpath = "// input[ @ type = 'submit']"
        button = self.driver.find_element_by_xpath(Xpath)
        button.click()


        #Select Addevent or Myevents
        Xpath = "// a[text()='Add event']"
        #Xpath = "// a[text()='My events']"
        button = self.driver.find_element_by_xpath(Xpath)
        button.click()


        #Add Event details

        input_dict = {'name': 'New Event Name',
                        'day': '25',
                        'month': '12',
                        'year': '2019',
                        'price': '0',
                        'numTickets': '400',
                        #'starthour': '20',
                        #'startminute': '30',
                        'customField': 'Tell me the name of your kid!',
                        'max_sell': '2',}


        #populate input tags
        Xpath = "// input[@type = 'text']"
        inputs = self.driver.find_elements_by_xpath(Xpath)
        for i in inputs:
            try:
                i.send_keys(input_dict[i.get_attribute('name')])
            except:
                pass


        #populate select tags
        selecttags = ['day', 'month', 'year', ]
        for value in selecttags:
            select = Select(self.driver.find_element_by_xpath("//select[@name='"+value+"']"))
            select.select_by_value(input_dict[value])

        #populate time hack
        #tab after year to get hour, the tab again to get minute
        time_dict = {'name': 'New Event Name',
                        'hour': '20',
                        'minute': '30', }
        elem = self.driver.find_element_by_name("year")
        elem.send_keys(Keys.TAB, time_dict['hour'])  # tab over to hour, which is a not-visible element
        elem.send_keys(Keys.TAB*2, time_dict['minute'])  # tab over to minute, which is a not-visible element

        #Populate Description and T&Cs,
        # Xpath = "// textarea[@name = 'description']"
        # inputs = self.driver.find_elements_by_xpath(Xpath)
        # print(len(inputs))
        elem = self.driver.find_element_by_name("specifySaleStart")
        elem.send_keys(Keys.TAB, "It's gonna be fun")  # tab over to description, which is a not-visible element
        elem = self.driver.find_element_by_name("specifySaleStart")
        elem.send_keys(Keys.TAB*2, "NO REFUNDS \n You break it, you bought it")  # tab over to terms

        #Submit
        Xpath = "// input[ @ type = 'submit']"
        button = self.driver.find_element_by_xpath(Xpath)
        button.click()




        time.sleep(100000)
        self.driver.quit()

        end = time.time()
        print('Worker finished : {} seconds'.format(int(end - start)))



def main():
    URL = "http://aphasian.com/ticketlab"
    USER = "leehayes81@hotmail.com"
    PASSWORD = "lmi123!!"
    t = BuyTickets(URL+"/buy/id/370")
    #t = CreateEvent(URL+"/login", USER, PASSWORD)
    t()


#view purchased tickets
#contact PVA

"As a user I need to...."


if __name__ == '__main__':
    main()
