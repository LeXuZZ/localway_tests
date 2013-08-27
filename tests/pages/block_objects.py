from selenium.webdriver import ActionChains

__author__ = 'lxz'


class HeaderBlock():

    header_leisure_link = lambda self: self.webdriver.find_element_by_xpath("//header/section/nav/a[1]")
    header_active_link = lambda self: self.webdriver.find_element_by_xpath("//header/section/nav/a[2]")
    header_restaurants_link = lambda self: self.webdriver.find_element_by_xpath("//header/section/nav/a[3]")
    header_hotels_link = lambda self: self.webdriver.find_element_by_xpath("//header/section/nav/a[4]")
    header_events_link = lambda self: self.webdriver.find_element_by_xpath("//header/section/nav/a[5]")
    header_journeys_link = lambda self: self.webdriver.find_element_by_xpath("//header/section/nav/a[6]")
    header_around_link = lambda self: self.webdriver.find_element_by_xpath("//header/section/nav/a[7]")
    header_more_link = lambda self: self.webdriver.find_element_by_xpath("//header/section/nav/a[8]")

    header_logo_link = lambda self: self.webdriver.find_element_by_xpath("//header/section[2]/ul/li[1]/a")
    header_change_city_link = lambda self: self.webdriver.find_element_by_xpath("//header/section[2]/ul/li[2]/div")
    header_register_link = lambda self: self.webdriver.find_element_by_xpath("//header/section[2]/ul/li[4]")
    header_login_link = lambda self: self.webdriver.find_element_by_xpath("//header/section[2]/ul/li[5]")
    header_language_link = lambda self: self.webdriver.find_element_by_xpath("//header/section[2]/ul/li[6]")


class FooterBlock():

    footer_leisure_link = lambda self: self.webdriver.find_element_by_xpath("//footer/section/nav/a[1]")
    footer_active_link = lambda self: self.webdriver.find_element_by_xpath("//footer/section/nav/a[2]")
    footer_restaurants_link = lambda self: self.webdriver.find_element_by_xpath("//footer/section/nav/a[3]")
    footer_hotels_link = lambda self: self.webdriver.find_element_by_xpath("//footer/section/nav/a[4]")
    footer_events_link = lambda self: self.webdriver.find_element_by_xpath("//footer/section/nav/a[5]")
    footer_journeys_link = lambda self: self.webdriver.find_element_by_xpath("//footer/section/nav/a[6]")
    footer_around_link = lambda self: self.webdriver.find_element_by_xpath("//footer/section/nav/a[7]")

    footer_logo_link = lambda self: self.webdriver.find_element_by_xpath("//footer/section[2]/a")


class PhotoGallery():

    gallery_main = lambda self: self.webdriver.find_element_by_xpath('//lw-gallery/div')
    gallery_previous = lambda self: self.webdriver.find_element_by_xpath('//a[@class=\'slide-prev\']')
    gallery_next = lambda self: self.webdriver.find_element_by_xpath('//a[@class=\'slide-next\']')
    move_to_thumbnails = lambda self: ActionChains(self.webdriver).move_to_element(self.webdriver.find_element_by_xpath(
        '//div[@class=\'thumbnails\']')).perform()
    thumbnails_previous = lambda self: self.webdriver.find_element_by_xpath('//div[@class=\'thumbnails\']/a[1])')
    thumbnails_next = lambda self: self.webdriver.find_element_by_xpath('//div[@class=\'thumbnails\']/a[2]')
    thumbnails_list = lambda self: self.webdriver.find_elements_by_xpath('//div[@class=\'thumbs-list\']/a')
    get_images = lambda self: self.webdriver.find_elements_by_xpath('//div[@class=\'img-container\']/img')
    get_circles = lambda self: self.webdriver.find_elements_by_xpath(
        '//div[@class=\'see-all\']/div[@class=\'circles\']/span')

    get_center_image = lambda self: self.get_images()[1]

