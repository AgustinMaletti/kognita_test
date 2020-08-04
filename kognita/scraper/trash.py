# def get_comment_question(page):
# 	'''
# 	Defines the selection of the comment data in the question
# 	:param page: is a source page with parsel Selector class wrapper
# 	:return: comment_list: is the list of comment data
# 	'''
# 	question_body = page.xpath('//div[@class="post-layout"]')
# 	question_comments = question_body.xpath('//div[contains(@class, "comment-body")]')
# 	comment_list = []
# 	for c in question_comments:
# 		comment = {'text': "", 'author': "", 'date': ""}
# 		comment['text'] = c.xpath('.//span[@class="comment-copy"]/text()').get()
# 		comment['author'] = c.xpath('.//a[contains(@class, "comment-user")]/text()').get()
# 		comment['date'] = c.xpath('.//span[contains(@class, "relativetime")]/text()').get()
# 		comment_list.append(comment)
# 	return {'question_comments': comment_list}


# def get_answers_and_comments_from_answers(page):
# 	'''
# 	Defines the selection of all answer in the page selecting the data and also
# 	getting all comments data in earch answer
# 	:param page: is the source page with a parsel Selctor wrapper
# 	:return all_answer_data: is  a list with the answer text, user, date and a list of comments
# 	'''
#
# 	answers = page.xpath('//div[@class="answer"]')
# 	all_answer_data = []
# 	for a in answers:
# 		answer_data = {'answer_text': "", 'answer_user': "", 'answer_date': "", 'answer_comments': ""}
# 		answer_data['answer_text'] = ''.join(a.xpath('.//div[@class="post-text"]//text()').getall())
# 		answer_user_info = a.xpath('.//div[contains(@class, "user-info")]')
# 		answer_data['answer_use'] = answer_user_info.xpath('.//div[@class="user-details"]/a/text()').get()
# 		answer_data['answer_date'] = answer_user_info.xpath('.//div[@class="user-action-time"]/span/text()').get()
# 		comment_in_answer_list = a.xpath('.//div[contains(@class,"comment-body")]')
# 		comments_in_answer = []
# 		for i, comment_in_answer in enumerate(comment_in_answer_list):
# 			comment_in_answer_text = comment_in_answer.xpath('.//span[@class="comment-copy"]/text()').get()
# 			comment_in_answer_author = comment_in_answer.xpath('.//a[@class="comment-user"]/text()').get()
# 			comment_in_answer_date = comment_in_answer.xpath('.//span[contains(@class, "relativetime")]/text()').get()
# 			comment_data = {'text': comment_in_answer_text, 'author': comment_in_answer_author,
# 							'date': comment_in_answer_date }
# 			comments_in_answer.append(comment_data)
# 		answer_data['answer_comments'] = comments_in_answer
# 		all_answer_data.append(answer_data)
# 	return {'all_answer': all_answer_data}



# def get_question_data(page):
# 	'''
# 	Defines the selection of the question data
# 	:param page: is the source page with a parsel Selector class wrapper
# 	:return question_data: is a dictionary with the data title, text. tags. date. and comments
# 	'''
# 	question_data = {'question_title':"", 'question_text':"", 'question_tags': "", 'question_date':"" , 'question_comments': ""}
# 	question_body = page.xpath('//div[@class="post-layout"]')
# 	question_data['question_title'] = page.xpath('//div[@id="question-header"]').xpath('.//a[contains(@class, "question")]/text()').get()
# 	question_data['question_text'] = ''.join(page.xpath('//div[@class="post-text"]').xpath('.//text()').getall())
# 	question_data['question_tags'] = page.xpath('//div[@class="post-layout"]').xpath('.//a[contains(@class, "post-tag")]//text()').getall()
# 	question_data['question_date'] = get_question_date(page)
# 	question_data['question_comments'] = get_comment_question(question_body.xpath('//div[contains(@class, "comment-body")]'))
# 	return question_data


#
# def get_question_date(page):
# 	'''
# 	Defines the selection of the date in questions layout
# 	:param page: is the source_page wrapped by a parsel Selector class
# 	:return date: is an string
# 	 '''
# 	data = page.xpath('//div[contains(@class, "post-layout--right")]')\
# 	.xpath('.//div[@class="user-action-time"]') \
# 	.xpath('.//span[@class="relativetime"]//text()').getall()
# 	data.reverse()
# 	return data[0]


# question_data = get_question_data(page)
# # return a list of dictionary
# question_comment = get_comment_question(page)
# # return a  list of dictionary and un key with the list of comments dictionary
# answers_data_and_comments = get_answers_and_comments_from_answers(page)

# print(f'Getting question and answer data in question number {i}')
		# data['question'].update(question_data)
		# data['question'].update(question_comment)
		# data['question'].update(answers_data_and_comments)