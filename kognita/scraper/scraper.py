
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from parsel import Selector
from time import sleep
import json

path_to_driver = '/home/baltasar/Desktop/ScrapyBoy/kognita/kognita/scraper/geckodriver'
driver = webdriver.Firefox(executable_path=path_to_driver)
file_name_data = 'data.json'
keyword = 'python'
# DATA STRUCTURE
"""
	Define the creation of the next data structure:

	data = {"initial_search": {"search_query": "",
    	                       "search_title_result": "",
        	                   "search_text_result": ""},
                            
                  "question": {"question_title": "",
			         		   "question_text": "",
					    	   "question_author": "",
						       "question_date": "",
						       "question_tags": "" ,
						       "question_comments": [{"text": "",
											"         author":"",
											          "date": ""}],
          				       "all_answer": [{"answer_text": "",
                          			     	   "answer_author": "",
                           				       "answer_date": "",
                           				       "answer_comments": [{"text": "",
                                            	    			     "author":"",
                                                 	     			 "date": ""
												 			               }],
                         				  }]
                        }
        }
	"""
def init_file(file_name:str):
	'''
	Defines the creation of an json file with an empy list inside
	:param file_name: is the name of the json file

	'''
	with open(file_name, mode='w', encoding='utf-8') as file:
		json.dump([], file)


def append_to_json(file_name:str, data):
	'''
	Defines the loading and appending method used for updating the file
	:param file_name: is the name of the json file to wich we append
	:param data: is the dictionary of data we are appending	
	'''
	with open(file_name, 'r', encoding='utf-8') as feedjson:
		feeds = json.load(feedjson)
	with open(file_name, 'w', encoding='utf-8') as outfile:
		feeds.append(data)
		json.dump(feeds, outfile, ensure_ascii=False, indent=4)


def create_dict():
	'''
	Defines the creation of a dict inside a dict for saving our data
	'''
	data = { "question": {
						  }
		    }

	return data

def initial_search(keyword:str):
	'''
	Define getting the page making the search and parseing some data, lastly return the questions links
	:param keyword is the searching word in the search box of stack overflow
	:return page is the source_page wrapped by a parsel Selector class
	
	'''
	# actions
	driver.get('https://stackoverflow.com/')
	driver.find_element_by_xpath('//input[@name="q"]').click()
	driver.find_element_by_xpath('//input[@name="q"]').send_keys(keyword)
	driver.find_element_by_xpath('//input[@name="q"]').send_keys(Keys.ENTER)
	print('Waiting 10, 9, 8...')
	sleep(10)
	# data

	page = Selector(driver.page_source)

	return page

def save_search_data(keyword, file_name):
	'''
		Defines the saving of the initial searhc data
	   :param keyword: is the keyword of the search
	   :param file_name is the json file we are using for saving the data
	'''
	data = {}
	data['search_query'] = keyword
	data['search_title_result'] = page.xpath('//h1//text()').get().strip()
	data['search_text_result'] = page.xpath('//div[@class="mb24"]').xpath('.//p//text()').get()
	append_to_json(file_name, data)


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


def get_comment_question(page):
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
	return {'question_comments': comment_list}


def get_answers_and_comments_from_answers(page):
	'''
	Defines the selection of all answer in the page selecting the data and also
	getting all comments data in earch answer
	:param page: is the source page with a parsel Selctor wrapper
	:return all_answer_data: is  a list with the answer text, user, date and a list of comments
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
	return {'all_answer': all_answer_data}



def get_question_data(page):
	'''
	Defines the selection of the question data
	:param page: is the source page with a parsel Selector class wrapper
	:return question_data: is a dictionary with the data title, text. tags. date. and comments
	'''
	question_data = {'question_title':"", 'question_text':"", 'question_tags': "", 'question_date':"" , 'question_comments': ""}
	question_body = page.xpath('//div[@class="post-layout"]')
	question_data['question_title'] = page.xpath('//div[@id="question-header"]').xpath('.//a[contains(@class, "question")]/text()').get()
	question_data['question_text'] = ''.join(page.xpath('//div[@class="post-text"]').xpath('.//text()').getall())
	question_data['question_tags'] = page.xpath('//div[@class="post-layout"]').xpath('.//a[contains(@class, "post-tag")]//text()').getall()
	question_data['question_date'] = get_question_date(page)
	question_data['question_comments'] = get_comment_question(question_body.xpath('//div[contains(@class, "comment-body")]'))
	return question_data

if __name__ == "__main__":
	# make the initial search
	print('Starting Stack Overflow Scraper')
	init_file(file_name_data)
	save_search_data(keyword, file_name_data)
	page = initial_search(keyword)
	all_questions_links = []
	# Get all links to questions in this page
	questions_links = get_questions_links(page)
	# save the links
	all_questions_links.extend(questions_links)
	print('Starting collecting questions links')
	for i in range(3):
		# get the number of the current page
		current_page = page.xpath('//div[contains(@class, "s-pagination--item is-selected")]/text()').get()
		# check it: if the current page is above two proceed to next page and extract and save more links
		if int(current_page) < 2:
			# get the relative link to next page
			next_href = page.xpath('//a[@rel="next"]/@href').get()
			# create the absolute link to next page
			next_page = 'https://stackoverflow.com' + next_href
			print('Going to next page for collecting more links')
			driver.get(next_page)
			print('Waiting 10, 9, 8 ...')
			sleep(10)
			page = Selector(driver.page_source)
			# Get all links to questions in this page
			questions_links = get_questions_links(page)
			# save the links in the main list
			all_questions_links.extend(questions_links)
			print(f'Getting question links on page {current_page}')

	print('I will start visiting links of question for getting the data')
	# now we have all links, now is time for getting the data of each question
	for i, link_to_question in enumerate(all_questions_links[:10]):
		data = create_dict()
		print(f'Going to link of question number {i+1}')
		driver.get(link_to_question)
		print('Waiting 10, 9, 8...')
		sleep(4)
		source_page = driver.page_source
		page = Selector(source_page)
		# return a dictionary
		question_data = get_question_data(page)
		# return a list of dictionary
		question_comment = get_comment_question(page)
		# return a  list of dictionary and un key with the list of comments dictionary
		answers_data_and_comments = get_answers_and_comments_from_answers(page)
		print(f'Getting question and answer data in question number {i}')
		data['question'].update(question_data)
		data['question'].update(question_comment)
		data['question'].update(answers_data_and_comments)

		print('Appending data to json file')
		append_to_json(file_name_data, data)

	print('Process finish Sr!')




		# for each question extract answer author text and day
		# for each answer extract comment author text and day
		







