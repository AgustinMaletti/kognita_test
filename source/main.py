# from scraper.selenium_scraper.scraper import path_to_driver
from source.config import BASE_DIR_DATA
# from source.scraper.selenium_scraper.test_path_resolve import FILE_DATA_NAME
from time import sleep
import argparse
from source.api_flask.app import app
from source.scraper.selenium_scraper.scraper import StackOverFlowScraper

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--execute", type=str, required=True,
                        help="Escolhe um programa para executar de las siguientes opciones, scraper_selenium, scraper_scrapy, flask_api")
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
            if '.' in file_name:
                file_name = file_name.split('.')[0]
                file_name = file_name + '.json'
            print('Your config is:')
            print('keyword: ', keyword)
            print('Question per page:', option)
            print('File name ', file_name)

            print('Its Ok, yes or no')
            ok_or_not = input()
            if ok_or_not == 'yes':
                break
            else:
                continue
        print('Loading config')

        scraper = StackOverFlowScraper(keyword=keyword, file_name=file_name, option=option)
        scraper.runt()

    elif args.execute == 'flask_api':
        print('Flask api choosed')
        app.run(debug=True)
    else:
        print('Please choose a valid option')





