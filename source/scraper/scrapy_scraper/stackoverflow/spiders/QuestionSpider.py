# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy import Request
from scrapy import Selector
import requests


class QuestionSpider(Spider):
    name = 'QuestionSpider'
    allowed_domains = ['stackoverflow.com']
    start_urls = ['https://stackoverflow.com/questions/tagged/python/']

    def start_requests(self):
        url = 'https://stackoverflow.com/questions/tagged/python'
        tag = getattr(self, 'tag', None)
        if tag is not None:
            url = f'https://stackoverflow.com/questions/tagged/{tag}'
        yield Request(url, self.parse)


    def parse(self, response):
        for href in response.xpath('//a[@class="question-hyperlink"]/@href').getall():
            yield Request(response.urljoin(href), self.parse_data)

        current_page =  int(response.xpath('//div[contains(@class, "s-pagination--item is-selected")]/text()').get())
        if current_page <= 2:
            next_page = response.xpath('//a[@rel="next"]/@href').get()
            yield Request(response.urljoin(next_page), self.parse)

    def get_comment_data(self, page_frag):
        comment_list = []
        for comment in page_frag.xpath('.//div[contains(@class, "comment-text")]'):
            comment_data = {}
            # for comments inside comments list: comment text
            comment_data['text'] = comment.xpath('.//div[contains(@class, "comment-body")]/span/text()').get()
            # for comments inside comments list: comment author
            comment_data['author'] = comment.xpath('.//div[contains(@class, "comment-body")]/a/text()').get()
            # for comments inside comments list: relativetime
            comment_data['date'] = comment.xpath('.//span[contains(@class, "relativetime")]/text()').get()
            comment_list.append(comment_data)
        return comment_list


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
                more_button = post.xpath('.//a[contains(@class,"js-show-link")]//text()[contains(., "show")]')

                # inside layout_body: comments list
                if  len(more_button) == 0:
                    comment_list = self.get_comment_data(page_frag=post)
                    data['question']['question_comments'] = comment_list
                else:
                    question_id = response.xpath('//div[@class="question"]/@data-questionid').get()
                    resp = requests.get(f'https://stackoverflow.com/posts/{question_id}/comments')
                    page_frag  = Selector(resp)
                    comment_list = self.get_comment_data(page_frag=page_frag)
                    data['question']['question_comments'] = comment_list

            else:
                answer = {}
                answer['text'] = ''.join(post.xpath('.//div[@class="post-text"]//text()').getall()).strip()
                answer_author_body = post.xpath('.//div[contains(@class,"user-info")]')
                answer['author'] = answer_author_body.xpath('.//div[@class="user-details"]/a/text()').get()
                answer['author_link'] = answer_author_body.xpath('.//div[@class="user-details"]/a/@href').get()
                answer['author_reputation'] = answer_author_body.xpath('.//span[@class="reputation-score"]/text()').get()
                answer['date'] = answer_author_body.xpath('.//span[@class="relativetime"]/text()').get()
                comment_list = self.get_comment_data(page_frag=post)
                 # inside layout_body: comments list
                if  len(more_button) == 0:
                    comment_list = self.get_comment_data(page_frag=post)
                    answer['comments'] = comment_list
                else:
                    question_id = response.xpath('//div[@class="question"]/@data-questionid').get()
                    resp = requests.get(f'https://stackoverflow.com/posts/{question_id}/comments')
                    page_frag  = Selector(resp)
                    comment_list = self.get_comment_data(page_frag=page_frag)
                    answer['comments'] = comment_list
                all_answers.append(answer)
        data['question']['all_answers'] = all_answers
        user_link = response.xpath('//div[@itemprop="author"]/a/@href').get()
        yield Request(response.urljoin(user_link), self.parse_more_user_info, cb_kwargs=dict(data=data))

    def parse_more_user_info(self, response, data):
        # page = self.selenium_get(response)
        data['question']['answers_made'] = response.xpath('//div[contains(@class,"fs-body3")]/text()').getall()[0]
        data['question']['question_made'] = response.xpath('//div[contains(@class,"fs-body3")]/text()').getall()[1]
        data['question']['people_reached'] = response.xpath('//div[contains(@class,"fs-body3")]/text()').getall()[2]
        data['question']['member_since'] = response.xpath('//div[contains(text(), "Member")]/span/text()').get()
        data['question']['profile_view'] = response.xpath('//div[contains(text(), "profile view")]/text()').get()
        data['question']['last_see'] = response.xpath('//div[contains(text(), "Last")]/span/text()').get()
        yield data

