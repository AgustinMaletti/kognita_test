from unittest import TestCase
from source.config import DIR_DATA
from source.config import GECKO_DRIVER
from source.scraper.selenium_scraper.scraper import StackOverFlowScraper
from time import sleep
from parsel import Selector
import json
import os
import io
import sys


class Test_Scraper(TestCase):

    def init_scraper(self):
        keyword='python'
        file_name = str(DIR_DATA.joinpath('test_data.json'))
        option = '15'
        headOption =  True
        maximum_question = '10'
        scraper = StackOverFlowScraper(keyword=keyword, file_name=file_name, option=option, geckoDriver=GECKO_DRIVER,
                                       headOption=headOption, maximum_question=maximum_question)
        return scraper

    def setUp(self):
        self.scraper = self.init_scraper()
        sleep(5)


    def tearDown(self):
        self.scraper.driver.close()
        if os.path.exists(self.scraper.file_name):
            os.remove(self.scraper.file_name)


    def test_comment_is_hide(self):
        self.scraper.driver.get('https://stackoverflow.com/questions/35753/is-python-good-for-big-software-projects-not-web-based')
        page = Selector(self.scraper.driver.page_source)
        comment = '''Re: "professional" -- I think (and it was a while back) I meant some combination of native and aesthetically 
                     pleasing. As of the writing of the original post I'd not seen any Python GUI app that was both -- in fact, most 
                     of them looked functional but crude. This may have changed, but I've been using CPython on the back end of web apps 
                     almost exclusively for the last couple of years, so I can't really say. '''
        comment_selected = page.xpath('//*[@id="comment-19115454"]/div[2]/div/span[1]').getall()
        self.assertNotIn(comment, comment_selected)


    def test_more_button_is_clicked(self):
        self.scraper.driver.get('https://stackoverflow.com/questions/35753/is-python-good-for-big-software-projects-not-web-based')
        self.scraper.look_for_more_btn_and_click()
        page = Selector(self.scraper.driver.page_source)
        # this is oart of a comment only available by clicking in more button
        comment = 'Re: "professional" -- I think (and it was a while back)'
        comment_selected = page.xpath('//*[@id="comment-19115454"]/div[2]/div/span[1]/text()').get()
        self.assertIn(comment, comment_selected)


    def test_parse_data(self):
        self.scraper.driver.get('https://stackoverflow.com/questions/35753/is-python-good-for-big-software-projects-not-web-based')
        page = Selector(self.scraper.driver.page_source)
        data = self.scraper.parse_data(page)
        question_title = 'Is Python good for big software projects'
        self.assertIn(question_title, data['question']['question_title'])


    def test_init_file(self):
        self.scraper.init_file(self.scraper.file_name)
        self.assertTrue(os.path.exists(self.scraper.file_name))


    def test_saving_data(self):
        self.scraper.driver.get('https://stackoverflow.com/questions/35753/is-python-good-for-big-software-projects-not-web-based')
        page = Selector(self.scraper.driver.page_source)
        data = self.scraper.parse_data(page)
        self.scraper.init_file(self.scraper.file_name)
        self.scraper.append_to_json(data)
        with open(self.scraper.file_name, 'r', encoding='utf-8') as file:
            data = json.load(file)
        question = "Is Python good for big software projects (not web based)? [closed]"
        self.assertIn(question, data[0]['question']['question_title'])


    def test_initial_search(self):
        self.scraper.initial_search(keyword='python')
        self.assertEquals(self.scraper.driver.current_url ,'https://stackoverflow.com/questions/tagged/python')


    def test_set_up_question_per_page_30(self):
        self.scraper.initial_search(keyword='python')
        self.scraper.setup_question_per_page_option('30')
        self.assertIn('30', self.scraper.driver.current_url)

    def test_get_user_data(self):
        data = {'question':{}}
        link = 'https://stackoverflow.com/users/10838965/frankenstein'
        data = self.scraper.get_user_detail(data, link)
        print_in_test(data)
        self.assertIn('year', data['question']['user_member_since'])
        





def print_in_test(hello):
    ''' Capture print statement in test '''
    captured_output = io.StringIO()                  # Create StringIO object
    sys.stdout = captured_output                     #  and redirect stdout.
    print(hello)                                     # Call unchanged function.
    sys.stdout = sys.__stdout__                      # Reset redirect.
    print('Captured', captured_output.getvalue())