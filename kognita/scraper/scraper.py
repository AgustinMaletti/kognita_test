
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from parsel import Selector
from time import sleep
import json
import argparse

# Setup the browser
# path to browser bin
path_to_driver = '/home/baltasar/Desktop/ScrapyBoy/kognita/kognita/scraper/geckodriver'
# file for saving data
file_name_data = 'data2.json'
# keyword for search
keyword = 'python'
# Defines the options and preference for the firefox browser
options = Options()
firefox_profile = webdriver.FirefoxProfile()
firefox_profile.DEFAULT_PREFERENCES['frozen']["javascript.enabled"] = True
options.profile = firefox_profile

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

def save_search_data(keyword, file_name, page):
	'''
		Defines the saving of the initial searhc data
	   :param keyword: is the keyword of the search
	   :param file_name is the json file we are using for saving the data
	'''
	data = {}
	data['search_query'] = keyword
	data['search_title_result'] = page.xpath('//h1[contains(@class,"grid--cell")]/text()').get().strip()
	data['search_text_result'] = page.xpath('//div[@class="mb24"]//p//text()').get().strip()
	append_to_json(file_name, data)


def get_questions_links(page):
	'''
	Defines getting and creating absolutes links for the questions
	:param page: is the source_page wrapped by a parsel Selector class
	:return questions_links: is a list with the a full url to each question link
	'''
	questions_links = ['https://stackoverflow.com' + link for link in page.xpath("//a[@class='question-hyperlink']/@href").getall()]
	return questions_links


def look_for_more_btn_and_click():
	'''
	Defines clicking in all more button in the comments for reveling more comments

	'''
	more_button_list = driver.find_elements_by_xpath('//a[contains(@class,"js-show-link comments-link") and contains(text(),"show")]')
	for more_btn in more_button_list:
		driver.execute_script("arguments[0].scrollIntoView();", more_btn)
		sleep(2)
		more_btn.click()
		sleep(2)


def parse_data(page):
	'''
	Defines the parsing of the data in the question page, first get the question and them the answers,
	also click in alll more buttons from comments and them itinerate over comments them for getting the info.
	:param page: is the source page wrapped by a selector class parsel
	:return data: is a dictionary with all the data in the page
	'''

	data = create_dict()
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
	data['question']['all_asnwers'] = all_answers
	return data


def setup_question_per_page_option(option):
	'''
    In the result page of the search, this function set up the
    quantity of question per page
    :param option: is the string number 15 or 30 or 50 for the total question by page
    :return page is the source apge wraped by a selector parsel class

    '''
	try:
		# close popup element if is there
		popup_element = driver.find_element_by_xpath('//a[contains(@class,"s-btn s-btn__muted")]')
		popup_element.click()
	except:
		pass
	if option == '15':
		pass
	elif option == '30':
		print('Setting 30 question by page')
		question_30 = driver.find_element_by_xpath('//a[contains(@title, "Show 30")]')
		driver.execute_script("arguments[0].scrollIntoView", question_30)
		sleep(3)
		question_30.click()
		sleep(3)
	elif option == '50':
		print('Setting 50 question by page')
		question_50 = driver.find_element_by_xpath('//a[contains(@title, "Show 50")]')
		driver.execute_script("arguments[0].scrollIntoView", question_50)
		sleep(3)
		question_50.click()
		sleep(3)
	return Selector(driver.page_source)
if __name__ == "__main__":
	# getting argument from command line
	parser = argparse.ArgumentParser()
	parser.add_argument("--question_by_page", type=str, help="Quantidade de perguntas por pagina, opcoes validas: 15, 30 e 50")
	parser.add_argument("--keyword", type=str, help="the keyword for the search")
	args = parser.parse_args()
	# the keyword for making the searc
	if args.keyword:
		keyword = args.keyword
	# the quenaitty of questions per page in the results page of the search
	if (args.question_by_page != '15' and args.question_by_page != '30' and args.question_by_page != '50'):
	# default value is 15
		question_by_page = '15'
		print('Setting default value of question by page equal 15')
	else:
		question_by_page = args.question_by_page

	driver = webdriver.Firefox(executable_path=path_to_driver, options=options)

	# make the initial search
	print('Starting Stack Overflow Scraper')
	init_file(file_name_data)
	page = initial_search(keyword)
	save_search_data(keyword, file_name_data, page)
	all_questions_links = []
	# Get all links to questions in this page
	page = setup_question_per_page_option(question_by_page)
	questions_links = get_questions_links(page)
	# save the links
	all_questions_links.extend(questions_links)
	print('Starting collecting questions links')
	for i in range(3):
		try:
			# get the number of the current page
			current_page = page.xpath('//div[contains(@class, "s-pagination--item is-selected")]/text()').get()
			# check it: if the current page is above two proceed to next page and extract and save more links
			if int(current_page) <= 2:
				print(f'Current number page is {current_page}')
				# get the relative link to next page
				next_href = page.xpath('//a[@rel="next"]/@href').get()
				# create the absolute link to next page
				next_page = 'https://stackoverflow.com' + next_href
				print('Going to next page for collecting more links')
				driver.get(next_page)
				print('Waiting 10, 9, 8 ...')
				sleep(10)
				page = Selector(driver.page_source)
				# set question per page equal to question_by_page
				# Get all links to questions in this page
				questions_links = get_questions_links(page)
				# save the links in the main list
				all_questions_links.extend(questions_links)
				print(f'Getting question links on page {current_page}')
		except KeyboardInterrupt:
			print('Closing Scraper')
			driver.close()
		except Exception:
			pass
	print('I will start visiting links of question for getting the data')
	# now we have all links, now is time for getting the data of each question
	for i, link_to_question in enumerate(all_questions_links):
		try:
			print(f'Going to link of question number {i+1}')
			driver.get(link_to_question)
			print('Waiting 4, 3, 2...')
			sleep(4)
			# the next function look for more buttons in comments scroll into view and click them
			look_for_more_btn_and_click()
			sleep(1)
			# we get the source page again becouse of the possible new comments redered
			source_page = driver.page_source
			page = Selector(source_page)
			data = parse_data(page)
			print('Appending data to json file')
			append_to_json(file_name_data, data)
		except KeyboardInterrupt:
			print('Closing Scraper')
			driver.close()
		except Exception:
			pass


	print('Process finish Sr!')











