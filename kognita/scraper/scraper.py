
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pathlib
import os
from parsel import Selector


path_to_driver = '/home/baltasar/Desktop/ScrapyBoy/kognita/kognita/scraper/geckodriver'
driver = webdriver.Firefox(executable_path=path_to_driver)
# STRUCTURE
dados = {"initial_search": {"search_query": "",
                            "search_title_result": "",
                            "search_text_result": "",       
                            
        "all_questions": [{ "question_title": "",
                            "question_preview_text": "",
                            "question_text": "",
                            "question_autor": "",
                            "question_data": "", 
                            "question_tags": "" ,
                            "question_comments": [{ "comment": "",
                                                    "comment_author":"",                                                    
                                                    "comment_data": ""
													}],
                           "answer_text": "",
                           "answer_author": "",
                           "answer_data": "",
                           "answer_comments": [{ "comment": "",
                                                 "comment_author":"",
                                                 "comment_data": ""
												 }],
                        }]
                        }
        }

def initial_search(keyword:str):
	'''
	Define geting the page making the search and parseing some data, lastly return the questions links
	:param keyword is the searching word in the search box of stack overflow
	:return question_links a list of full links to each question present in page
	
	'''
	driver.get('https://stackoverflow.com/')
	driver.find_element_by_xpath('//input[@name="q"]').click()
	driver.find_element_by_xpath('//input[@name="q"]').send_keys(keyword)
	driver.find_element_by_xpath('//input[@name="q"]').send_keys(Keys.ENTER)
	dados['initial_search']['search_query'] = keyword	
	page = Selector(driver_page_source)
	dados['inital_search']['search_title_result'] = page.xpath('//h1//text()').get().strip()
	dados['inital_search']['search_text_result'] = page.xpath('//div[@class="mb24"]').xpath('.//p//text()').get()
	return driver.page_source
	
def get_questions_links(page):
	'''
	Defines getting and creating absolutes links for the questions
	:param page is the source_page wrapped by a parsel Selector class
	:return questions_links are the fullpath link to the questions
	'''
	questions_links = ['https://stackoverflow.com' + link for link in page.xpath("//a[@class='question-hyperlink']/@href").getall()]
	return questions_links

def get_date(page):

	data = page.xpath('//div[contains(@class, "post-layout--right")]')\
	.xpath('.//div[@class="user-action-time"]') \
	.xpath('.//span[@class="relativetime"]//text()').getall()
	data.reverse()
	return data[0]

def get_comment_question(question_comments):

	comment_list = []
	for c in question_comments:
		comment = {'text': "", 'author': "", 'time': ""}
		comment['text'] = c.xpath('.//span[@class="comment-copy"]/text()').get()
		comment['author'] = c.xpath('.//a[contains(@class, "comment-user")]/text()').get()
		comment['time'] = c.xpath('.//span[contains(@class, "relativetime")]/text()').get()
		comment_list.append(comment)	
	return comment_list

def get_answers_and_comments_from_asnwers(page):
	answers = page.xpath('//div[@class="answer"]')
	for a in answers:
		answer_text = ''.join(a.xpath('.//div[@class="post-text"]//text()').getall()))
		answer_user_info = a.xpath('.//div[contains(@class, "user-info")]')
		answer_user = answer_user_info.xpath('.//div[@class="user-details"]/a/text()').get())
		answer_data = answer_user_info.xpath('.//div[@class="user-action-time"]/span/text()').get())
		comment_in_answer_list = a.xpath('.//div[contains(@class,"comment-body")]')
		for i, comment_in_answer in enumerate(comment_in_answer_list):
			comment_in_answer_text = comment_in_answer.xpath('.//span[@class="comment-copy"]/text()').get()
			comment_in_answer_author = comment_in_answer.xpath('.//a[@class="comment-user"]/text()').get()
			comment_in_answer_data = comment_in_answer.xpath('.//span[contains(@class, "relativetime")]/text()').get()
			

def get_question(page):
	'''
	:param page is the source page with a parsel Slector wrapper
	'''
	question = {'question_title':"", 'question_text':"", 'question_tags': "", 'question_date':"" , 'question_comments': ""}
	question_body = page.xpath('//div[@class="post-layout"]')
	question['question_title'] = page.xpath('//div[@id="question-header"]').xpath('.//a[contains(@class, "question")]/text()').get()
	question['question_text'] = ''.join(page.xpath('//div[@class="post-text"]').xpath('.//text()').getall())
	question['question_tags'] = page.xpath('//div[@class="post-layout"]').xpath('.//a[contains(@class, "post-tag")]//text()').getall()
	question['question_date'] = get_data(page_source)
	question['question_comments'] = get_comment_question(question_body.xpath('//div[contains(@class, "comment-body")]'))
	return question

if __name__ == "__main__":
	# make the initial search
	driver_source_page = initial_search('python')
	# Get all links to questions in this page
	page = Selector(driver_source_page)
	all_questions_links = []
	for i in range(3):
		# get the number of the current page
		current_page = int(page.xpath('//div[contains(@class, "s-pagination--item is-selected")]//text()').get())
		# check it: if the current page is above two proceed to next page and extract and save more links
		if int(current_page) < 2:
			# get the relative link to next page
			next_href = page.xpath('//a[@rel="next"]//@href').get()
			# create the absolute link to next page
			next_page = 'https://stackoverflow.com' + next_href
			driver_source_page	= driver.get(next_page)
			page = Selector(driver_source_page)
			# Get all links to questions in this page
			questions_links = get_questions_links(driver_source_page)
			# save the links in the main list
			all_questions_links.append(questions_links)
	# now we have all links, now is time for getting the data of each question
	for link in all_questions_links():
		driver.get(link)
		source_page = driver.page_source
		page = Selector(source_page)
		questions_links = get_questions_links(page)



		# for each question extract answer author text and day
		# for each answer extract comment author text and day
		







