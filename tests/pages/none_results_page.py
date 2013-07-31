# coding=utf-8
import re
from wtframework.wtf.web.page import PageObject, InvalidPageError

__author__ = 'lxz'


class NoneResultsList(PageObject):


        ### Page Elements Section ###
    search_what_input = lambda self: self.webdriver.find_element_by_id(
        "input-what")
    search_where_input = lambda self: self.webdriver.find_element_by_id(
        "input-where")
    search_button = lambda self: self.webdriver.find_element_by_xpath(
        "//button[@class=\"btn-search\"]")
    ### End Page Elements Section ###

    def _validate_page(self, webdriver):

        '''
        Validates we are on the correct page.
        '''

        if not re.search('Localway', webdriver.title):
            raise InvalidPageError('This page did not pass NoneResultsListPage page validation.')

    def check_text_presence(self):
        if not u'Вы искали' in self.webdriver.find_element_by_xpath('/html/body/div/section/h2').text:
            raise InvalidPageError('This page did not pass NoneResultsListPage page validation.')
        if not u'0 Результатов' in self.webdriver.find_element_by_xpath('/html/body/div/section/div/h2').text:
            raise InvalidPageError('This page did not pass NoneResultsListPage page validation.')
        if not u'К сожалению, по Вашему запросу ничего не найдено.\nВозможно, вы допустили ошибку в слове, исправьте ее и попробуйте найти снова.' in self.webdriver.find_element_by_xpath('/html/body/div/section/div/p').text:
            raise InvalidPageError('This page did not pass NoneResultsListPage page validation.')
