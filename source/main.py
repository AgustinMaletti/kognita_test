# from scraper.selenium_scraper.scraper import path_to_driver
from source.config import BASE_DIR_DATA
from source.scraper.selenium_scraper.test_path_resolve import FILE_DATA_NAME
import argparse






if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--optional", type=str,
                        help="Quantidade de perguntas por pagina, opcoes validas: 15, 30 e 50")
    args = parser.parse_args()
    # print('args are', args)
    print(args.optional)
    print(BASE_DIR_DATA)
    print(FILE_DATA_NAME)
