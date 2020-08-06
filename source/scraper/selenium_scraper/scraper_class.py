from scrapy.linkextractors import LinkExtractor
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from parsel import Selector
from selenium.webdriver.firefox.options import Options
import pathlib
from source.config import BASE_DIR_DATA


class Scraper():
    def __init__(self, path_to_driver:str, destiny_folder:str, xpath: dict, next_limit:int, headless=False):
                 
        '''
        Prepare the browser for operations, initial setup, and one call to init search
        :param xpath input_pattern, links_pattern, next_pattern, body_pattern, data_pattern_list 
        '''
        self.xpath = xpath
        self.next_limit = next_limit
        options = Options()
        firefox_profile = webdriver.FirefoxProfile()
        firefox_profile.DEFAULT_PREFERENCES['frozen']["javascript.enabled"] = True
        options.profile = firefox_profile
        options.headless = headless
        self.driver = webdriver.Firefox(executable_path=path_to_driver, options=options)
        sleep(10)

    def __rpr___(self):
        ''':param
        The representation of the object put here
        all the information that you wont to follow'''
        pass

    def init_search(self, keyword: str, url: str, xpath ):
        '''
        Go to site click search and write the query and press enter
        :param keyword is the searching word in the search box of stack overflow
        :param url is self explained
        :param xpath is the input box,
        :return source

        '''
        # actions
        self.driver.get(url)
        sleep(5)
        self.driver.find_element_by_xpath(self.xpath['input_pattern']).click()
        self.driver.find_element_by_xpath(self.xpath['input_pattern']).send_keys(keyword)
        self.driver.find_element_by_xpath(self.xpath['input_pattern']).send_keys(Keys.ENTER)
        print('Waiting 10, 9, 8...')
        sleep(10)
        # data
        source = self.driver.page_source
        return source

    def extract_links(self, xpath, source, domain, relative=True):

        '''
        Defines getting and creating absolutes links for the questions
        :param page: is the source_page wrapped by a parsel Selector class
        :return questions_links: is a list with the a full url to each question link
        '''
        page = Selector(source)
        links = page.xpath(self.xpath['body_pattern']).getall()
        if relative:
            links = [domain + link for link in links]
        return links


    def next_loop(self):
        for i in range(self.next_limit):
            self.driver.get('')
            pass





