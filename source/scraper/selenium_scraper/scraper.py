
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from parsel import Selector
from time import sleep
import json
import os

# DATA STRUCTURE
"""
	Define the creation of the next data structure:

	data = {"initial_search": {"search_query": "",
    	                       "search_title_result": "",
        	                   "search_text_result": ""},

                  "question": {"question_title": "",
			         		   "question_text": "",
					    	   "question_author_name": "",
					    	   "question_author_link": "",
						       "question_date": "",
						       "question_tags": "" ,
						       "question_comments": [{"text": "",
											"         author":"",
											          "date": ""}],
											          
							   "user_answers_made": "",
            				   "user_questions_made": "",
            				   "user_people_reached": "",
            				   "user_member_since": "",
            				   "user_profile_view": "",
            				   "user_last_see": ""			          
          				       "all_answer": [{"answer_text": "",
                          			     	   "answer_author": "",
                           				       "answer_date": "",
                           				       "answer_comments": [{"text": "",
                                            	    			     "author":"",
                                                 	     			 "date": "",
												 			       }],
                        	  }]
                   }
    }
"""


class StackOverFlowScraper():

	def __init__(self,keyword:str, file_name:str, option:str, geckoDriver:str, headOption:bool, maximum_question=None, follow_user_data=False):
		'''
		:param option is 15 or 30 or 50 questions by page

		'''
		# Setup the browser
		self.keyword = keyword
		self.file_name = file_name
		self.option = option
		self.max_question = maximum_question
		self.follow_user_data = follow_user_data
		options = Options()
		firefox_profile = webdriver.FirefoxProfile()
		firefox_profile.DEFAULT_PREFERENCES['frozen']["javascript.enabled"] = True
		options.profile = firefox_profile
		headless = False if headOption else True
		options.headless = headless
		self.driver = webdriver.Firefox(executable_path=geckoDriver, options=options)



	def init_file(self, file_name):
		'''
		Defines the creation of an json file with an empy list inside
		:param file_name: is the name of the json file

		'''
		with open(file_name, mode='w', encoding='utf-8') as file:
			json.dump([], file)
		assert os.path.exists(file_name)


	def append_to_json(self, data):
		'''
		Defines the loading and appending method used for updating the file
		:param file_name: is the name of the json file to wich we append
		:param data: is the dictionary of data we are appending
		'''
		with open(self.file_name, 'r', encoding='utf-8') as feedjson:
			feeds = json.load(feedjson)
		with open(self.file_name, 'w', encoding='utf-8') as outfile:
			feeds.append(data)
			json.dump(feeds, outfile, ensure_ascii=False, indent=4)


	def initial_search(self, keyword):
		'''
		Define getting the page making the search and parseing some data, lastly return the questions links
		:param keyword is the searching word in the search box of stack overflow
		:return page is the source_page wrapped by a parsel Selector class

		'''
		# actions
		self.driver.get('https://stackoverflow.com/')
		sleep(5)
		assert self.driver.current_url == 'https://stackoverflow.com/'
		self.driver.find_element_by_xpath('//input[@name="q"]').click()
		self.driver.find_element_by_xpath('//input[@name="q"]').send_keys(keyword)
		self.driver.find_element_by_xpath('//input[@name="q"]').send_keys(Keys.ENTER)
		print('Waiting 10, 9, 8...')
		sleep(10)
		# data
		page = Selector(self.driver.page_source)
		return page

	def save_search_data(self, page):
		'''
			Defines the saving of the initial searhc data
		   :param keyword: is the keyword of the search
		   :param file_name is the json file we are using for saving the data
		'''
		data = {}
		data['search_query'] = self.keyword
		data['search_title_result'] = page.xpath('//h1[contains(@class,"grid--cell")]/text()').get().strip()
		data['search_text_result'] = page.xpath('//div[@class="mb24"]//p//text()').get().strip()
		self.append_to_json(data)

	def load_data(self, file_name):
		'''
			:param: file_name: the json file for loading
			:return: data list
		'''
		with open(file_name, 'r', encoding='utf-8') as file:
			data = json.load(file)
		return data

	def get_user_links(self, data):
		'''
		I use this method in the get user details method
		:param data is the json file loaded as a list with dicts insidde


		'''
		links = []
		for i, row in enumerate(data):
			try:
				links.append((i, row['question']['question_author_link']))
			except Exception:
				continue
		return links

	def get_user_detail(self, data, link):
		'''
		Defines loading the data from file and getting the links form the file, itinerate over links  and save new user info.
		:param file_name: is teh file from where load data

		'''
		try:
			print('following user detail link')
			self.driver.get(link)
			print('Waiting 7, 6, 5, 4, 3,...')
			sleep(7)
			page = Selector(self.driver.page_source)
			data['question']['user_answers_made'] = page.xpath('//div[contains(@class,"fs-body3")]/text()').getall()[0]
			data['question']['user_questions_made'] = page.xpath('//div[contains(@class,"fs-body3")]/text()').getall()[1]
			data['question']['user_people_reached'] = page.xpath('//div[contains(@class,"fs-body3")]/text()').getall()[2]
			data['question']['user_member_since'] = page.xpath('//div[contains(text(), "Member")]/span/text()').get()
			data['question']['user_profile_view'] = page.xpath('//div[contains(text(), "profile view")]/text()').get()
			data['question']['user_last_see'] = page.xpath('//div[contains(text(), "Last")]/span/text()').get()
			return data
		except Exception:
			pass

	def get_questions_links(self, page):
		'''
		Defines getting and creating absolutes links for the questions
		:param page: is the source_page wrapped by a parsel Selector class
		:return questions_links: is a list with the a full url to each question link
		'''
		questions_links = ['https://stackoverflow.com' + link for link in page.xpath("//a[@class='question-hyperlink']/@href").getall()]
		assert len(questions_links) == int(self.option)
		return questions_links


	def look_for_more_btn_and_click(self):
		'''
		Defines clicking in all more button in the comments for reveling more comments in the current url of the driver

		'''
		more_button_list = self.driver.find_elements_by_xpath('//a[contains(@class,"js-show-link comments-link") and contains(text(),"show")]')
		for more_btn in more_button_list:
			self.driver.execute_script("arguments[0].scrollIntoView();", more_btn)
			sleep(3)
			more_btn.click()
			sleep(3)


	def get_comment_data(self, page_frag):
		comment_list = []
		# inside layout_body: comments list
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
		
	
	

	def parse_data(self, page, follow_user_data:bool=False):
		'''
		Defines the parsing of the data in the question page, first get the question and them the answers,
		also click in alll more buttons from comments and them itinerate over comments them for getting the info.
		:param page: is the source page wrapped by a selector class parsel
		:return data: is a dictionary with all the data in the page
		'''

		data = {'question': { } }
		data['question']['question_title'] = page.xpath('//div[@id="question-header"]/h1/a/text()').get()
		all_answers = []
		posts = page.xpath('//div[@class="post-layout"]')
		for i, post in enumerate(posts):
			try:
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
					data['question']['question_author_link'] = 'https://stackoverflow.com' + question_author_body.xpath('.//div[@class="user-details"]/a/@href').get()
					# inside user_body: reputation points
					data['question']['question_author_reputation'] = question_author_body.xpath('.//span[@class="reputation-score"]/text()').get()
					# inside user_body: date
					data['question']['question_date'] = question_author_body.xpath('.//span[@class="relativetime"]/text()').get()
					# inside layout_body: comments list
					comment_list = self.get_comment_data(post)
					data['question']['question_comments'] = comment_list

				else:
					answer = {}
					answer['text'] = ''.join(post.xpath('.//div[@class="post-text"]//text()').getall()).strip()
					answer_author_body = post.xpath('.//div[contains(@class,"user-info")]')
					answer['author'] = answer_author_body.xpath('.//div[@class="user-details"]/a/text()').get()
					answer['author_link'] = answer_author_body.xpath('.//div[@class="user-details"]/a/@href').get()
					answer['author_reputation'] = answer_author_body.xpath('.//span[@class="reputation-score"]/text()').get()
					answer['date'] = answer_author_body.xpath('.//span[@class="relativetime"]/text()').get()
					comment_list = self.get_comment_data(post)
					answer['comments'] = comment_list
					all_answers.append(answer)
			except Exception:
				continue
			except KeyboardInterrupt:
				break
		data['question']['all_asnwers'] = all_answers
		if follow_user_data:
			link = data['question']['question_author_link']
			data = self.get_user_detail(data, link)
		return data


	def setup_question_per_page_option(self, option):
		'''
		In the result page of the search, this function set up the
		quantity of question per page
		:param option: is the string number 15 or 30 or 50 for the total question by page
		:return page is the source apge wraped by a selector parsel class

		'''
		try:
			# close popup element if is there
			popup_element = self.driver.find_element_by_xpath('//a[contains(@class,"s-btn s-btn__muted")]')
			popup_element.click()
		except:
			pass
		if option == '15':
			pass
		elif option == '30':
			print('Setting 30 question by page')
			question_30 = self.driver.find_element_by_xpath('//a[contains(@title, "Show 30")]')
			self.driver.execute_script("arguments[0].scrollIntoView", question_30)
			sleep(3)
			question_30.click()
			sleep(3)
			assert '30' in self.driver.current_url
		elif option == '50':
			print('Setting 50 question by page')
			question_50 = self.driver.find_element_by_xpath('//a[contains(@title, "Show 50")]')
			self.driver.execute_script("arguments[0].scrollIntoView", question_50)
			sleep(3)
			question_50.click()
			sleep(3)
			assert '50' in self.driver.current_url
		return Selector(self.driver.page_source)

	def run(self):
		'''
		Defines  Makingthe initial search, extracting links follow next page for more links until reach page 2.
		Follow links to each questions parsing the data and appending it to json file.

		'''

		# make the initial search
		print('Starting Stack Overflow Scraper')
		self.init_file(self.file_name)
		page = self.initial_search(self.keyword)
		self.save_search_data(page)
		all_questions_links = []
		# Get all links to questions in this page
		page = self.setup_question_per_page_option(self.option)
		questions_links = self.get_questions_links(page)
		# save the links
		all_questions_links.extend(questions_links)
		print('Starting collecting questions links')
		for i in range(3):
			try:
				# get the number of the current page
				current_page = int(page.xpath('//div[contains(@class, "s-pagination--item is-selected")]/text()').get())
				# check it: if the current page is above two proceed to next page and extract and save more links
				if current_page <= 2:
					print(f'Current number page is {current_page}')
					# get the relative link to next page
					next_href = page.xpath('//a[@rel="next"]/@href').get()
					# create the absolute link to next page
					next_page = 'https://stackoverflow.com' + next_href
					print('Going to next page for collecting more links')
					self.driver.get(next_page)
					print('Waiting 10, 9, 8 ...')
					sleep(10)
					page = Selector(self.driver.page_source)
					# set question per page equal to question_by_page
					# Get all links to questions in this page
					questions_links = self.get_questions_links(page)
					# save the links in the main list
					all_questions_links.extend(questions_links)
					print(f'Getting question links on page {current_page}')
			except KeyboardInterrupt:
				print('Closing Scraper')
				self.driver.close()
			except Exception as error:
				print(f'I catch this error: {error}')
				continue
		print('I will start visiting links of question for getting the data')
		# now we have all links, now is time for getting the data of each question
		maximum_question  = int(self.max_question) if self.max_question is not None else len(all_questions_links)
		for i, link_to_question in enumerate(all_questions_links[:maximum_question]):
			try:
				print(f'Going to link of question number {i + 1}')
				self.driver.get(link_to_question)
				print('Waiting 4, 3, 2...')
				sleep(4)
				# the next function look for more buttons in comments scroll into view and click them
				self.look_for_more_btn_and_click()
				sleep(1)
				# we get the source page again becouse of the possible new comments redered
				source_page = self.driver.page_source
				page = Selector(source_page)
				data = self.parse_data(page, follow_user_data=self.follow_user_data)
				print('Appending data to json file')
				self.append_to_json(data=data)
			except KeyboardInterrupt:
				print('Closing Scraper')
				self.driver.close()
			except Exception as error:
				print(f'I catch this error: {error}')
				continue
		print('Process finish Sr!')
		self.driver.close()













