
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
	questions_links = ['https://stackoverflow.com' +link for link in page.xpath("//a[@class='question-hyperlink']/@href").getall()]
	return questions_links
	
all_questions_links= []	

if __name__ == "__main__":
	# the title and the preview text, if the current page number is above 2 do it again	
	driver_source_page = initial_search('python')
	# Get all links to questions
	questions_links = parse_page(driver_source_page)
	all_questions_links.append(questions_links)
	current_page = page.xpath('//div[contains(@class, "s-pagination--item is-selected")]//text()').get()
	next_href = page.xpath('//a[@rel="next"]//@href').get()
	next_page = 'https://stackoverflow.com'' + next_href
	if int(current_page) < 2:
		driver_ source_page	= driver.get(next_page)
		questions_links = parse_page(driver_source_page)
		all_questions_links.append(questions_links)
	
	for link in all_questions_links():
		source_page







