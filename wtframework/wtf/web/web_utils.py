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
from urllib2 import urlopen
import urllib2
import re
from wtframework.wtf.web.page import PageFactory
from wtframework.wtf.config import WTF_TIMEOUT_MANAGER
import time
from threading import Thread
from datetime import datetime, timedelta

class WebUtils(object):


    @staticmethod
    def check_url(url):
        '''
        Check if resource at URL is fetchable. (by trying to fetch it and checking for 200 status.
        @param url: Url to check.
        @type url: str
        @return: Returns a tuple of {success, response code}
        @rtype: Tuple
        '''
        request = urllib2.Request(url)
        try:
            response = urlopen(request)
            return True, response.code
        except urllib2.HTTPError as e:
            return False, e.code

    @staticmethod
    def get_base_url(webdriver):
        """
        Get the current base URL.
        @param webdriver: Selenium webdriver.
        """
        current_url = webdriver.current_url
        try:
            return re.findall("^[^/]+//[^/$]+", current_url)[0]
        except:
            raise RuntimeError("Unable to process base url: {0}".format(current_url) )

    @staticmethod
    def is_webdriver_mobile(webdriver):
        """
        Check if a web driver if mobile.
        @param webdriver: Selenium webdriver.
        """
        browser = webdriver.capabilities['browserName']

        if browser == u'iPhone' or \
        browser == u'android':
            return True
        else:
            return False

    @staticmethod
    def is_webdriver_ios(webdriver):
        """
        Check if a web driver if mobile.
        @param webdriver: Selenium webdriver.
        """
        browser = webdriver.capabilities['browserName']

        if browser == u'iPhone' or \
        browser == u'iPad':
            return True
        else:
            return False


    @staticmethod
    def switch_to_window(page_class, webdriver):
        """
        @param page_class: Page class to search for/instantiate.
        @param webdriver: Selenium webdriver.
        """
        window_list = list(webdriver.window_handles)
        original_window = webdriver.current_window_handle
        for window_handle in window_list:
            webdriver.switch_to_window(window_handle)
            try:
                return PageFactory.create_page(page_class, webdriver)
            except:
                pass
        
        webdriver.switch_to_window(original_window)
        raise WindowNotFoundError("Window {0} not found.")
    

class BrowserStandBy(object):
    """
    This class allows you to put a browser on stand by sending no-op commands to keep 
    a selenium session from timing out.
    """
    
    def __init__(self, webdriver, max_time=WTF_TIMEOUT_MANAGER.EPIC, sleep=5):
        """
        @param webdriver:Webdriver instance to keep alive. 
        """
        self.webdriver = webdriver
        self._sleep_time = sleep
        self._max_time = max_time
        
        
    
    def start(self):
        """
        Start standing by.  A periodic command like 'current_url' will be sent to the 
        webdriver instance to prevent it from timing out.
        """
        self._end_time = datetime.now() + timedelta(seconds = self._max_time)
        self._thread = Thread(target=lambda: self.__stand_by_loop())
        self._keep_running = True
        self._thread.start()
        pass
    
    def stop(self):
        "Stop BrowserStandBy from sending additional calls to webdriver."
        self._keep_running = False
        pass
    
    
    def __stand_by_loop(self):
        print self._keep_running
        while datetime.now() < self._end_time and self._keep_running:
            self.webdriver.current_url #Just performing current_url to keep this alive.
            time.sleep(self._sleep_time)


class WindowNotFoundError(RuntimeError):
    "Raised when window is not found by web_utils script."


