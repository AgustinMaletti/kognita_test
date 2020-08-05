import json
import os
import pandas as pd
from pprint import pprint
from pathlib import Path

print(Path(__file__).resolve().parent)

parent_fodler = Path(__file__).resolve().parent
json_file = Path.joinpath(parent_fodler, 'data_scraper_selenium.json')

def load_data(json_file):
    with open(json_file, 'r', encoding='utf-8') as feedjson:
        feeds = json.load(feedjson)
        return feeds

data = load_data(json_file=json_file)
result_data_scraper_selenium = data[1:]

result_data_scraper_scrapy =''





















# pprint(result_data_scraper_selenium[:3])

# for i, row in enumerate(result_data_scraper_selenium[:3]):
#     print(i, row['question']['question_author_name'])


# def get_author_question(author_name, data):
#     results = []
#     for i, row in enumerate(data):
#         if author_name == row['question']['question_author_name']:
#             results.append(data[i])
#     if len(results) > 0:
#         print(f'This user make {len(results)} questions')
#         for question in results:
#             print(question)
#         return results
#     else:
#         return None

# print(len(result_data_scraper_selenium))
# get_author_question(author_name="Viktor Oláh", data=result_data_scraper_selenium)



# search_data = {'search_query': feeds[0]['search_query'], 'search_title_result': feeds[0]['search_title_result'], 'search_text_result': feeds[0]['search_text_result']}
# print(type(result_data))
# pprint(result_data)
# "John"
# print(type(feeds))
# print(feeds)
# pprint(feeds)
# print(feeds[0])
# result_query = get_author_question("John")
# print(result_query)
# print(result_query['question'].keys())
# for i in list(result_query['question'].keys()):
#     print(i, '-'*136)
#     print(result_query['question'][i])
# print(os.path.abspath(__file__).parent)
# data_file = os.path.join(os.getcwd(), 'data_scraper_selenium.json')
# print('file_dir', data_file)
# df = pd.read_json(data_file)
# print(df.head())

# for i in result_data_scraper_selenium:
#     print(i['question'])
