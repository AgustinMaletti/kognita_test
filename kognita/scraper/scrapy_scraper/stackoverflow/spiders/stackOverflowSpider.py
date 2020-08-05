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

path_to_driver = '/home/baltasar/Desktop/ScrapyBoy/kognita/kognita/scraper/geckodriver'


class StackoverflowspiderSpider(CrawlSpider):
    name = 'stackOverflowSpider'
    allowed_domains = ['https://stackoverflow.com/questions/tagged/python']
    start_urls = ['http://https://stackoverflow.com/questions/tagged/python/']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//a[@rel="next"]/@href'), follow=True),
        Rule(LinkExtractor(restrict_xpaths="//a[@class='question-hyperlink']/@href"), callback='parse_data', follow=True)
            )

    def __init___(self, *args, **kwargs):
        super(StackoverflowspiderSpider, self).__init__(*args, **kwargs)
        options = Options()
        firefox_profile = webdriver.FirefoxProfile()
        firefox_profile.DEFAULT_PREFERENCES['frozen']["javascript.enabled"] = True
        options.profile = firefox_profile
        self.driver = webdriver.Firefox(executable_path=path_to_driver, options=options)

    def selenium_get(self, response):
        self.driver.get(response.url)
        sleep(7)
        source_page = self.driver.page_source
        page = Selector(source_page)
        return page

    def parse_data(self, response):
        page = self.selenium_get(response)
        data = {'question': {}}
        data['question']['question_title'] = page.xpath('//div[@id="question-header"]/h1/a/text()').get()
        all_answers = []
        for i, post in enumerate(page.xpath('//div[@class="post-layout"]')):
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

        user_link = page.xpath('//div[@itemprop="author"]/a/@href').get()
        return response.follow(user_link, self.parse_more_user_info, cb_kwargs=dict(data=data))

    def parse_more_user_info(self, response, data):
        page = self.selenium_get(response)
        data['question']['answers_made'] = page.xpath('//div[contains(@class,"fs-body3")]/text()').getall()[0]
        data['question']['question_made'] = page.xpath('//div[contains(@class,"fs-body3")]/text()').getall()[1]
        data['question']['people_reached'] = page.xpath('//div[contains(@class,"fs-body3")]/text()').getall()[2]
        data['question']['member_since'] = page.xpath('//div[contains(text(), "Member")]/span/text()').get()
        data['question']['profile_view'] = page.xpath('//div[contains(text(), "profile view")]/text()').get()
        data['question']['last_see'] = page.xpath('//div[contains(text(), "Last")]/span/text()').get()
        return data


process = CrawlerProcess(settings={ "CLOSESPIDER_PAGECOUNT":30,
                                    "FEEDS": {"items.json": {"format": "json"},},
                                   }
                        )

if __name__ == "__main__":
    process.crawl(StackoverflowspiderSpider)
    process.start()