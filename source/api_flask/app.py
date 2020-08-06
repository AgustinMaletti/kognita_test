from flask import jsonify
from flask import current_app
import json
from flask import Blueprint

main = Blueprint('main', __name__)

@main.route('/')
def index():

    return '<h1>Hello Kognita</h1>'

@main.route('/get_data/<author_name>', methods=['GET'])
def get_data(author_name):
    '''
    Defines retriving th questions from the user query and returning it if is there
    :param author_name: is the query to make to the data
    '''
    file_name = current_app.config['file_name']
    total_data = load_data(json_file=file_name)
    partial_data = get_author_question(author_name, total_data[1:])
    if partial_data is not None:
        response = jsonify(partial_data), 200
    else:
        response = {"data": "No data for that user"}, 404
    return response

@main.route('/user_list', methods = ['GET'])
def user_list():
    '''
    Defines retiving the user list available in data file
    '''
    file_name = current_app.config['file_name']
    data = load_data(file_name)
    author_list = get_author_list(data[1:])
    response = jsonify(author_list), 200
    return response


def load_data(json_file):
    '''
    Defines loading and returning the json file
    :param json_file: is self explained

    '''

    with open(json_file, 'r', encoding='utf-8') as feedjson:
        feeds = json.load(feedjson)
        return feeds

def get_author_question(author_name, data):
    '''
    Define itinerating over each row of the json and checking if the user match. Return a list of results or Noene.
    :param auhtor_name: is  the query to check in the question_auhtor_name key
    :param data:  is the total_data json file loaded
    :return None or results

    '''
    results = []
    for i, row in enumerate(data):
        if author_name == row['question']['question_author_name']:
            results.append(data[i])
    if len(results) > 0:
        return results
    else:
        return None

def get_author_list(data):
    '''
    Query all authors and append them
    :param data: is the json file loaded
    :return author list: is a dict with a key author list and a list of authors as a values

    '''
    author_list = {'author_list': []}
    for i in data:
        author_list['author_list'].append(i['question']['question_author_name'])
    return author_list



