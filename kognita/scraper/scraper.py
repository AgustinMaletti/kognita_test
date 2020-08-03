
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pathlib
import os


path_to_driver = '/home/baltasar/Desktop/ScrapyBoy/kognita/kognita/scraper/geckodriver'
driver = webdriver.Firefox(executable_path=path_to_driver)

dados = {"initial_search": {"search_query": ""
                            "search_title_result": "",
                            "search_text_result": "",       
                            
        "all_questions": [{ "question_title": "",
                            "question_preview_text": "",
                            "question_text": "",
                            "question_autor": "",
                            "question_data": "", 
                            "question_tags": "" 
                            "question_comments": [{ "comment": "",
                                                    "comment_author":"",                                                    
                                                    "comment_data": "" }]
                           "answer_text": "",
                           "answer_author": "",
                           "answer_data": "",
                           "answer_comments": [{ "comment": "",
                                                    "comment_author":"",                                                    
                                                    "comment_data": "" }]
                        
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
	
def parse_page(driver_page_source):
	'''
	Defines getting and creating absolutes links for the questions
	:param driver_page_source
	:return questions_links
	'''
	questions_links = ['https://stackoverflow.com' + link for link in page.xpath("//a[@class='question-hyperlink']/@href").getall()]
	return questions_links


def get_data(page_source):
	data = page_source.xpath('//div[contains(@class, "post-layout--right")]')\
	.xpath('.//div[@class="user-action-time"]') \
	.xpath('.//span[@class="relativetime"]//text()').getall()
	data.reverse()
	return data[0]


def get_comment_question(question_comments)	
	comment_list = []
	for c in question_comments:
		comment = {'text': "", 'author': "", 'time': ""}
		comment['text'] = c.xpath('.//span[@class="comment-copy"]/text()').get()
		comment['author'] = c.xpath('.//a[contains(@class, "comment-user")]/text()').get()
		comment['time'] = c.xpath('.//span[contains(@class, "relativetime")]/text()').get()
		comment_list.append(comment)	
	return comment_list

def 
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
			


	
#def parse_question_page(source_page):
		
	
	
	
all_questions_links= []	

if __name__ == "__main__":
	# make the initial search
	driver_source_page = initial_search('python')
	# Get all links to questions in this page
	questions_links = parse_page(driver_source_page)
	# save the links in the main list
	all_questions_links.append(questions_links)
	# check the number of the current page
	current_page = page.xpath('//div[contains(@class, "s-pagination--item is-selected")]//text()').get()
	# get the relative link to next page
	next_href = page.xpath('//a[@rel="next"]//@href').get()
	# create the absolute link to next page
	next_page = 'https://stackoverflow.com'' + next_href
	# if the current page is above two proceed to next page and extract and save more links
	if int(current_page) < 2:
		driver_source_page	= driver.get(next_page)
		questions_links = parse_page(driver_source_page)
		all_questions_links.append(questions_links)
	# now we have all links, now is time for getting the data of each question
	for link in all_questions_links():
		driver.get(link)
		source_page = driver.page_source
		page = Selector(source_page)
		question_body = page.xpath('//div[@class="post-layout"]')
		question_title = page.xpath('//div[@id="question-header"]').xpath('.//a[contains(@class, "question")]/text()').get()
		question_text = ''.join(page.xpath('//div[@class="post-text"]').xpath('.//text()').getall())
		question_tags = page.xpath('//div[@class="post-layout"]').xpath('.//a[contains(@class, "post-tag")]//text()').getall()
		question_data = get_data(page_source)
		question_comments = get_comment_question(question_body.xpath('//div[contains(@class, "comment-body")]'))
		# for each question extract answer author text and day
		# for each answer extract comment author text and day
		







