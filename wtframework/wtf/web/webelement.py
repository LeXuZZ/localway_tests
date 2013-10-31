##########################################################################
#This file is part of WTFramework. 
#
#    WTFramework is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    WTFramework is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with WTFramework.  If not, see <http://www.gnu.org/licenses/>.
##########################################################################
from datetime import datetime, timedelta
from selenium.common.exceptions import ElementNotSelectableException, \
    TimeoutException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.expected_conditions import _find_element
from selenium.webdriver.support.wait import WebDriverWait
from wtframework.wtf.config import WTF_TIMEOUT_MANAGER
import time


class WebElementSelector():
    @staticmethod
    def find_element_by_selectors(webdriver, *selectors):
        """
        Utility method makes it easier to find an element using multiple selectors. This is 
        useful for problematic elements what might works with one browser, but fail in another.
        
        Usage:
            my_element = WebElementSelector.find_element_by_selectors(webdriver,
                                                                    (By.ID, "MyElementID"),
                                                                    (By.CSS, "MyClassSelector") )

        @param webdriver: Selenium WebDriver.
        @param selectors: Selectors as a variable arg list of (By, value) pairs.
        """
        #perform initial check to verify selectors are valid by statements.
        for selector in selectors:
            (by_method, value) = selector
            if not WebElementSelector.__is_valid_by_type(by_method):
                raise BadSelectorError("Selectors should be of type selenium.webdriver.common.by.By")
            if type(value) != str:
                raise BadSelectorError("Selectors should be of type selenium.webdriver.common.by.By")

        selectors_used = []
        for selector in selectors:
            (by_method, value) = selector
            selectors_used.append("{by}:{value}".format(by=by_method, value=value))
            try:
                return webdriver.find_element(by=by_method, value=value)
            except:
                pass

        raise ElementNotSelectableException("Unable to find elements using:" + ",".join(selectors_used))

    @staticmethod
    def __is_valid_by_type(by_type):
        for attr, value in By.__dict__.iteritems():
            if "__" not in attr:
                if by_type == value:
                    return True

        return False


class WebElementUtils():
    """
    Utility methods for working with web pages and web elements.
    """


    @staticmethod
    def wait_until_element_not_visible(webdriver, locator_lambda_expression, \
                                       timeout=WTF_TIMEOUT_MANAGER.NORMAL, sleep=0.5):
        "Wait for a WebElement to disappear."
        # Wait for loading progress indicator to go away.
        try:
            stoptime = datetime.now() + timedelta(seconds=timeout)
            while datetime.now() < stoptime:
                element = WebDriverWait(webdriver, WTF_TIMEOUT_MANAGER.BRIEF).until(locator_lambda_expression)
                if element.is_displayed():
                    time.sleep(sleep)
                else:
                    break
        except TimeoutException:
            pass

    @staticmethod
    def check_exists_by_xpath(webdriver, xpath):
        try:
            webdriver.find_element_by_xpath(xpath)
        except NoSuchElementException:
            return False
        return True

    @staticmethod
    def is_image_loaded(webdriver, webelement):
        '''
        Check if an image (in an image tag) is loaded.
        Note: This call will not work against background images.  Only Images in <img> tags.

        @param webelement: WebDriver web element to validate.
        @type webelement: WebElement
        '''
        script = "return arguments[0].complete && type of arguments[0].naturalWidth != \"undefined\" " + \
                 "&& arguments[0].naturalWidth > 0"
        try:
            return webdriver.execute_script(script, webelement)
        except:
            return False #Img Tag Element is not on page.

    @staticmethod
    def check_is_displayed(webdriver, element, message='element is disabled', timeout=1):
        find = lambda self, e=element: False if e.get_attribute("disabled") == 'true' else True
        WebDriverWait(webdriver, timeout).until(find, message)


    @staticmethod
    def check_if_attached_in_dom(webdriver, element, message='element is not attached in DOM', timeout=2):
        try:
            WebDriverWait(webdriver, timeout).until(freshness_of(element), message)
            return True
        except TimeoutException:
            return False

    @staticmethod
    def check_if_text_present_in_element_value(webdriver, locator, text, message='text not present in element value',
                                               timeout=2):
        try:
            WebDriverWait(webdriver, timeout).until(
                expected_conditions.text_to_be_present_in_element_value(locator, text), message)
            return True
        except TimeoutException:
            return False


class BadSelectorError(Exception):
    "Raised when a bad selector is passed into a WebElementSelector() method."
    pass


class freshness_of(object):
    """ Wait until an element is no longer attached to the DOM.
    element is the element to wait for.
    returns False if the element is still attached to the DOM, true otherwise.
    """
    def __init__(self, element):
        self.element = element

    def __call__(self, ignored):
        try:
            # Calling any method forces a staleness check
            self.element.is_enabled()
            return True
        except StaleElementReferenceException as expected:
            return False


class text_to_be_present_in_one_of_elements(object):
    """ An expectation for checking if the given text is present in the
    specified elements.
    elements, text
    """
    def __init__(self, elements, text_):
        self.elements = elements
        self.text = text_

    def __call__(self, ignored):
        try:
            for element in self.elements:
                element_text = element.text
                return element_text in self.text
        except StaleElementReferenceException:
            return False