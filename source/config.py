from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DIR_DATA = BASE_DIR.joinpath('data')
GECKO_DRIVER = BASE_DIR.joinpath('scraper', 'selenium_scraper', 'geckodriver')
FILE_FOR_API = DIR_DATA.joinpath('data3.json')