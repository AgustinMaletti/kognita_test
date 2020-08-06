# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from parsel import Selector
from time import sleep
from scrapy.crawler import CrawlerProcess
from scrapy import Spider
from scrapy import Request


path_to_driver = '/home/baltasar/Desktop/ScrapyBoy/kognita/kognita/scraper/geckodriver'


class StackoverflowspiderSpider(Spider):
    name = 'stackOverflowSpider'
    allowed_domains = ['stackoverflow.com']
    start_urls = ['https://stackoverflow.com/questions/tagged/python/']

    # *args, ** kwargs
    # def __init___(self):
    #     # super(StackoverflowspiderSpider, self).__init__(*args, **kwargs)
    #     options = Options()
    #     firefox_profile = webdriver.FirefoxProfile()
    #     firefox_profile.DEFAULT_PREFERENCES['frozen']["javascript.enabled"] = True
    #     options.profile = firefox_profile
    #     # self.driver = webdriver.Firefox(executable_path=path_to_driver, options=options)


    # def selenium_get(self, response):
    #     # self.driver.get(response.url)
    #     sleep(7)
    #     source_page = self.driver.page_source
    #     page = Selector(source_page)
    #     return page


    def parse(self, response):
        # page = self.selenium_get(response.url)

        for href in response.xpath('//a[@class="question-hyperlink"]').getall():
            yield Request(response.urljoin(href), self.parse_data)

        current_page =  int(response.xpath('//div[contains(@class, "s-pagination--item is-selected")]/text()').get())
        if current_response <= 2:
            next_page = response.xpath('//a[@rel="next"]').get()
            yield Request(response.urljoin(next_page), self.parse)


    def parse_data(self, response):
        # page = self.selenium_get(response)
        data = {'question': {}}
        data['question']['question_title'] = response.xpath('//div[@id="question-header"]/h1/a/text()').get()
        all_answers = []
        for i, post in enumerate(response.xpath('//div[@class="post-layout"]')):
            if i == 0:
                # inside layout_body: post text
                data['question']['question_text'] = ''.join(post.xpath('.//div[@class="post-text"]//text()').getall()).strip()
                # tags only in questions
                data['question']['question_tags'] = post.xpath('.//div[contains(@class, "post-taglist")]//a/text()').getall()
                # inside layout_body: user_body
                question_author_body = post.xpath('.//div[contains(@class,"user-info")]')
                # inside user_body: user name
                data['question']['question_author_name'] = question_author_body.xpath('.//div[@class="user-details"]/a/text()').get()
                # inside user_body: relative link to profile
                data['question']['question_author_link'] = question_author_body.xpath('.//div[@class="user-details"]/a/@href').get()
                # inside user_body: reputation points
                data['question']['question_author_reputation'] = question_author_body.xpath('.//span[@class="reputation-score"]/text()').get()
                # inside user_body: date
                data['question']['question_date'] = question_author_body.xpath('.//span[@class="relativetime"]/text()').get()

                comment_list = []
                # inside layout_body: comments list
                for comment in post.xpath('.//div[contains(@class, "comment-text")]'):
                    comment_data = {}
                    # for comments inside comments list: comment text
                    comment_data['text'] = comment.xpath('.//div[contains(@class, "comment-body")]/span/text()').get()
                    # for comments inside comments list: comment author
                    comment_data['author'] = comment.xpath('.//div[contains(@class, "comment-body")]/a/text()').get()
                    # for comments inside comments list: relativetime
                    comment_data['date'] = comment.xpath('.//span[contains(@class, "relativetime")]/text()').get()
                    comment_list.append(comment_data)
                data['question']['question_comments'] = comment_list
            else:
                answer = {}
                answer['text'] = ''.join(post.xpath('.//div[@class="post-text"]//text()').getall()).strip()
                answer_author_body = post.xpath('.//div[contains(@class,"user-info")]')
                answer['author'] = answer_author_body.xpath('.//div[@class="user-details"]/a/text()').get()
                answer['author_link'] = answer_author_body.xpath('.//div[@class="user-details"]/a/@href').get()
                answer['author_reputation'] = answer_author_body.xpath('.//span[@class="reputation-score"]/text()').get()
                answer['date'] = answer_author_body.xpath('.//span[@class="relativetime"]/text()').get()
                comment_list = []
                for comment in post.xpath('.//div[contains(@class, "comment-text")]'):
                    comment_data = {}
                    # for comments inside comments list: comment text
                    comment_data['text'] = comment.xpath('.//div[contains(@class, "comment-body")]/span/text()').get()
                    # for comments inside comments list: comment author
                    comment_data['author'] = comment.xpath('.//div[contains(@class, "comment-body")]/a/text()').get()
                    # for comments inside comments list: relativetime
                    comment_data['date'] = comment.xpath('.//span[contains(@class, "relativetime")]/text()').get()
                    comment_list.append(comment_data)
                answer['comments'] = comment_list
                all_answers.append(answer)
        data['question']['all_answers'] = all_answers
        user_link = response.xpath('//div[@itemprop="author"]/a/@href').get()
        yield response.follow(user_link, self.parse_more_user_info, cb_kwargs=dict(data=data))

    def parse_more_user_info(self, response, data):
        # page = self.selenium_get(response)
        data['question']['answers_made'] = response.xpath('//div[contains(@class,"fs-body3")]/text()').getall()[0]
        data['question']['question_made'] = response.xpath('//div[contains(@class,"fs-body3")]/text()').getall()[1]
        data['question']['people_reached'] = response.xpath('//div[contains(@class,"fs-body3")]/text()').getall()[2]
        data['question']['member_since'] = response.xpath('//div[contains(text(), "Member")]/span/text()').get()
        data['question']['profile_view'] = response.xpath('//div[contains(text(), "profile view")]/text()').get()
        data['question']['last_see'] = response.xpath('//div[contains(text(), "Last")]/span/text()').get()
        yield data


process = CrawlerProcess(settings={ "CLOSESPIDER_PAGECOUNT":30,
                                    "FEEDS": {"items.json": {"format": "json"},},
                                    "DOWNLOAD_DELAY": 5,
                                   }
                        )

if __name__ == "__main__":
    process.crawl(StackoverflowspiderSpider)
    process.start()




# def start_requests(self):
#     for link in start_
#
# rules = (
#     Rule(LinkExtractor(restrict_xpaths=['//a[@rel="next"]']), follow=True),
#     Rule(LinkExtractor(restrict_xpaths=['//a[@class="question-hyperlink"]']), callback='parse_data', follow=True)
#         )
