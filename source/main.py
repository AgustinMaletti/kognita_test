from time import sleep
import argparse
from source.api_flask import create_app
from source.scraper.selenium_scraper.scraper import StackOverFlowScraper
from pathlib import Path
import unittest
from source.api_flask.tests.tests import Test_Api
from source.scraper.selenium_scraper.tests.tests import Test_Scraper
import os


BASE_DIR = Path(__file__).resolve().parent
DIR_DATA = BASE_DIR.joinpath('data')
GECKO_DRIVER = BASE_DIR.joinpath('scraper', 'selenium_scraper', 'geckodriver')
FILE_FOR_API = DIR_DATA.joinpath('data4_python.json')


def suite_api():
    suite = unittest.TestSuite()
    suite.addTest(Test_Api('test_author_list_200'))
    suite.addTest(Test_Api('test_author_list_key_is_present'))
    suite.addTest(Test_Api('test_author_list_author_is_present'))
    suite.addTest(Test_Api('test_author_data_is_not_present'))
    suite.addTest(Test_Api('test_author_data_is_present'))
    return suite

def suite_scraper():
    suite = unittest.TestSuite()
    suite.addTest(Test_Scraper('test_comment_is_hide'))
    suite.addTest(Test_Scraper('test_more_button_is_clicked'))
    suite.addTest(Test_Scraper('test_parse_data'))
    suite.addTest(Test_Scraper('test_init_file'))
    suite.addTest(Test_Scraper('test_saving_data'))
    suite.addTest(Test_Scraper('test_initial_search'))
    suite.addTest(Test_Scraper('test_set_up_question_per_page_30'))
    suite.addTest(Test_Scraper('test_get_user_data'))

    return suite


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--execute", type=str, required=True,
                        help="Escolhe um programa para executar das siguintes opções: scraper, api, test_api, test_scraper")
    args = parser.parse_args()
    if  args.execute == 'scraper':
        print('Scraper Choosed')
        while True:
            print('Please enter a keyword to search in StackOverFlow:', end=' ')
            keyword = input('')
            sleep(1)
            print('How much questions do you wont per page, 15, 30 or 50:', end=' ')
            option = input('')
            print('Please enter the name of the file:', end=' ')
            file_name = input('')
            print('Do you wont to see the browser in action, yes or no:', end=' ')
            headOption = input('')
            if headOption == 'yes':
                headOption = True
            else:
                headOption = False

            if '.' in file_name:
                file_name = file_name.split('.')[0]
                file_name = f'{file_name}_{keyword}.json'
            else:
                file_name = f'{file_name}_{keyword}.json'

            print('Enter the maximun quantity of questions to visit or 0 (zero) for no limit:', end=' ')
            maximum_question = input('')
            maximum_question = None if not maximum_question.isdigit() else maximum_question
            maximum_question = None if maximum_question == '0' else maximum_question
            print('Do you wont to get aditional data from the user profiles? yes or no', end=' ')
            follow_user_data = input()
            follow_user_data = True if follow_user_data == 'yes' else False
            os.system('cls' if os.name == 'nt' else 'clear')
            print('Your config is: ')
            print('keyword: ', keyword)
            print('Question per page: ', option)
            print('File name: ', file_name)
            print('Head option: ', str(headOption))
            print('Maximun questions: ', maximum_question)
            print('Get aditional User data:', str(follow_user_data))
            print('Its Ok?, yes or no:')
            ok_or_not = input()
            if ok_or_not == 'yes':
                break
            else:
                continue
        os.system('cls' if os.name == 'nt' else 'clear')
        print('Loading config')
        file_name = str(Path.joinpath(DIR_DATA, file_name))
        scraper = StackOverFlowScraper(keyword=keyword, file_name=file_name, option=option, geckoDriver=GECKO_DRIVER, headOption=headOption, maximum_question=maximum_question, follow_user_data=follow_user_data)
        scraper.run()

    elif args.execute == 'api':
        print('Flask Api Choosed')
        app = create_app(FILE_FOR_API)
        app.run(debug=True)

    elif args.execute == 'test_api':
        print('Starting testing API')
        runner = unittest.TextTestRunner()
        runner.run(suite_api())

    elif args.execute == 'test_scraper':
        print('Starting testing Scraper')
        runner = unittest.TextTestRunner()
        runner.run(suite_scraper())

    else:
        print('Please choose a valid option')





