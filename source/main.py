# from scraper.selenium_scraper.scraper import path_to_driver
from source.config import BASE_DIR_DATA
# from source.scraper.selenium_scraper.test_path_resolve import FILE_DATA_NAME
import argparse
from source.api_flask.app import app






if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--execute", type=str, required=True,
                        help="Escolhe um programa para executar de las siguientes opciones, scraper_selenium, scraper_scrapy, flask_api")
    args = parser.parse_args()
    if  args.execute == 'scraper_selenium':
        print('Scraper Selenium escolhido')
    elif args.execute == 'scraper_scrapy':
        print('Scraper Scrapy escolhido')
    elif args.execute == 'flask_api':
        print('Flask api escolhida')
        app.run(debug=True)
    else:
        print('Por favor escolhe uma opção valida das siguintes\n\tscraper_selenium\n\tscraper_scrapy\n\tflask_api')





