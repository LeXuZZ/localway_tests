from random import choice
from string import lowercase
from hamcrest import *

__author__ = 'lxz'


def verify_if_displayed(element):
    assert_that(element().is_displayed(), is_(True), 'element is not displayed')


def verify_max_length_of_field(element, field_length=50):
    element().clear()
    random_text = "".join(choice(lowercase) for i in range(field_length + 5))
    element().send_keys(random_text)
    assert_that(element().get_attribute('value'), has_length(field_length))


def verify_if_disabled(element):
    assert_that(element().is_enabled(), is_(False), 'element is not disabled')


def verify_if_enabled(element):
    assert_that(element().is_enabled(), is_(True), 'element is not enabled')