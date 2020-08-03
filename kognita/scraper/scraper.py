
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pathlib
import os
from parsel import Selector
from time import sleep

path_to_driver = '/home/baltasar/Desktop/ScrapyBoy/kognita/kognita/scraper/geckodriver'
driver = webdriver.Firefox(executable_path=path_to_driver)
# STRUCTURE
dados = {"initial_search": {"search_query": "",
                            "search_title_result": "",
                            "search_text_result": "",       
                            
        "all_questions": [{ "question_title": "",
                            "question_preview_text": "",
                            "question_text": "",
                            "question_author": "",
                            "question_date": "",
                            "question_tags": "" ,
                            "question_comments": [{ "text": "",
                                                    "author":"",
                                                    "date": ""
													}],
          				   "all_answer": [{"answer_text": "",
                          				   "answer_author": "",
                           				   "answer_date": "",
                           				   "answer_comments": [{ "text": "",
                                            				     "author":"",
                                                 				 "date": ""
												 			   }],
                         				  }]
                        }]
        }}

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
	:param page: is the source_page wrapped by a parsel Selector class
	:return questions_links: is a list with the a full url to each question link
	'''
	questions_links = ['https://stackoverflow.com' + link for link in page.xpath("//a[@class='question-hyperlink']/@href").getall()]
	return questions_links

def get_question_date(page):
	'''
	Defines the selection of the date in questions layout
	:param page: is the source_page wrapped by a parsel Selector class
	:return date: is an string
	 '''
	data = page.xpath('//div[contains(@class, "post-layout--right")]')\
	.xpath('.//div[@class="user-action-time"]') \
	.xpath('.//span[@class="relativetime"]//text()').getall()
	data.reverse()
	return data[0]

def get_comment_question_list(page):
	'''
	Defines the selection of the comment data in the question
	:param page: is a source page with parsel Selector class wrapper
	:return: comment_list: is the list of comment data
	'''
	question_body = page.xpath('//div[@class="post-layout"]')
	question_comments = question_body.xpath('//div[contains(@class, "comment-body")]')
	comment_list = []
	for c in question_comments:
		comment = {'text': "", 'author': "", 'date': ""}
		comment['text'] = c.xpath('.//span[@class="comment-copy"]/text()').get()
		comment['author'] = c.xpath('.//a[contains(@class, "comment-user")]/text()').get()
		comment['date'] = c.xpath('.//span[contains(@class, "relativetime")]/text()').get()
		comment_list.append(comment)	
	return comment_list

def get_answers_and_comments_from_answers(page):
	'''
	Defines the selection of all answer in the page selecting the data and also
	getting all comments data in earch answer
	:param page: is the source page with a parsel Selctor wrapper
	:return all_answer_data: is  alist with the answer text, user, date and a list of comments
	'''

	answers = page.xpath('//div[@class="answer"]')
	all_answer_data = []
	for a in answers:
		answer_data = {'answer_text': "", 'answer_user': "", 'answer_date': "", 'answer_comments': ""}
		answer_data['answer_text'] = ''.join(a.xpath('.//div[@class="post-text"]//text()').getall())
		answer_user_info = a.xpath('.//div[contains(@class, "user-info")]')
		answer_data['answer_use'] = answer_user_info.xpath('.//div[@class="user-details"]/a/text()').get()
		answer_data['answer_date'] = answer_user_info.xpath('.//div[@class="user-action-time"]/span/text()').get()
		comment_in_answer_list = a.xpath('.//div[contains(@class,"comment-body")]')
		comments_in_answer = []
		for i, comment_in_answer in enumerate(comment_in_answer_list):
			comment_in_answer_text = comment_in_answer.xpath('.//span[@class="comment-copy"]/text()').get()
			comment_in_answer_author = comment_in_answer.xpath('.//a[@class="comment-user"]/text()').get()
			comment_in_answer_date = comment_in_answer.xpath('.//span[contains(@class, "relativetime")]/text()').get()
			comment_data = {'text': comment_in_answer_text, 'author': comment_in_answer_author,
							'date': comment_in_answer_date }
			comments_in_answer.append(comment_data)
		answer_data['answer_comments'] = comments_in_answer
		all_answer_data.append(answer_data)
	return all_answer_data



def get_question_data(page):
	'''
	Defines the selection of the question data
	:param page: is the source page with a parsel Selector class wrapper
	:return question_data: is a dictionary with the data title, text. tags. date. and comments
	'''
	question_data = {'question_title':"", 'question_text':"", 'question_tags': "", 'question_date':"" , 'question_comments': ""}
	question_body = page.xpath('//div[@class="post-layout"]')
	question['question_title'] = page.xpath('//div[@id="question-header"]').xpath('.//a[contains(@class, "question")]/text()').get()
	question['question_text'] = ''.join(page.xpath('//div[@class="post-text"]').xpath('.//text()').getall())
	question['question_tags'] = page.xpath('//div[@class="post-layout"]').xpath('.//a[contains(@class, "post-tag")]//text()').getall()
	question['question_date'] = get_data(page_source)
	question['question_comments'] = get_comment_question(question_body.xpath('//div[contains(@class, "comment-body")]'))
	return question_data

if __name__ == "__main__":
	# make the initial search
	driver_source_page = initial_search('python')
	page = Selector(driver_source_page)
	all_questions_links = []
	# Get all links to questions in this page
	questions_links = get_questions_links(page)
	# save the links
	all_questions_links.append(questions_links)
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
			questions_links = get_questions_links(page)
			# save the links in the main list
			all_questions_links.append(questions_links)
			print(f'Getting question links on page {current_page}')
			sleep(1)

	# now we have all links, now is time for getting the data of each question
	for i, link_to_question in enumerate(all_questions_links()):
		driver.get(link_to_question)
		source_page = driver.page_source
		page = Selector(source_page)
		question_data = get_question_data(page)
		question_comment = get_comment_question_list()
		answers_data_and_comments = get_answers_and_comments_from_answers(page)
		print(f'Getting question and answer data in question number {i}')
		sleep(2)




		# for each question extract answer author text and day
		# for each answer extract comment author text and day
		







