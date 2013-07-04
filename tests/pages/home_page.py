__author__ = 'lxz'

from wtframework.wtf.web.page import PageObject, InvalidPageError


class HomePage(PageObject):
    '''
    HomePage
    WTFramework PageObject representing a page like:
    http://172.31.237.12/
    '''


    ### Page Elements Section ###
    search_what = lambda self: self.webdriver.find_element_by_xpath("/html/body/div/section/section/div/div/form/input")
    search_where = lambda self: self.webdriver.find_element_by_xpath(
        "/html/body/div/section/section/div/div/form/input[2]")
    search_button = lambda self: self.webdriver.find_element_by_css_selector(
        "html>body>div>section>section>div>div>form>button>i")
    ### End Page Elements Section ###


    def _validate_page(self, webdriver):
        '''
        Validates we are on the correct page.
        '''

        if not 'http://172.31.237.12/' in webdriver.current_url:
            raise InvalidPageError("This page did not pass HomePage page validation.")

    def search_for_what(self, search_string):
        # We can call a mapped element by calling it's lambda function.
        self.search_what().send_keys(search_string)


    def search_for_where(self, search_string):
        # We can call a mapped element by calling it's lambda function.
        self.search_where().send_keys(search_string)

    def click_search_button(self):
        self.search_button().click()
