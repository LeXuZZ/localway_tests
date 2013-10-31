# coding=utf-8
import inspect
import shlex
import sys
from wtframework.wtf.web.page import PageFactory
from tests import pages
from tests.pages import home_page, HomePage
from wtframework.wtf.config import ConfigReader
from wtframework.wtf.testobjects.basetests import WTFBaseTest
from wtframework.wtf.web.webdriver import WTF_WEBDRIVER_MANAGER

__author__ = 'lxz'


class TestGenerator(WTFBaseTest):

    case_text = ['clear search_what_input',
                 'input "Bar" to search_what_input',
                 'clear search_where_input',
                 'input "Moscow" to search_where_input',
                 'click to search_button']


    maxDiff = None

    def set_up(self):
        webdriver = WTF_WEBDRIVER_MANAGER.new_driver()
        webdriver.get(ConfigReader('site_credentials').get("default_url"))
        return webdriver

    def test_generator(self):
        clsmembers = inspect.getmembers(sys.modules['tests.pages'], inspect.isclass)
        a = [x for x in clsmembers if not x[0].startswith('__') and not x[0] == 'block_objects']
        webdriver = self.set_up()
        for case in self.case_text:
            generate_test(case, HomePage)
        pass


def generate_test(case_text, klass):
    case_splitted = shlex.split(case_text)
    all_class_methods = [x for x in dir(klass) if not x.startswith('_')]
    if any(all_class_methods) in case_splitted:
        print '1'
    d = {}
    for y in all_class_methods:
        for x in case_splitted:
            if x == y:
                d['element_method'] = y
                break
    for i, x in enumerate(case_splitted):
        if x == 'click' or x == 'clear':
            d['action'] = x
        if x == 'input':
            d['action'] = 'send_keys'
            d['parameter'] = case_splitted[i + 1]
    do_action(d, klass)
    pass


def do_action(case_map, klass):
    page_object = PageFactory.create_page(klass)
    webelement = getattr(page_object, case_map['element_method'])()
    action = getattr(webelement, case_map['action'])
    if 'parameter' in case_map: action(case_map['parameter'])
    else: action()
    pass