from flask import Flask
from flask import jsonify
from flask import Request
from source.data.data import result_data_scraper_selenium

app = Flask(__name__)


@app.route('/index')
def index():
    # if Request.method == "GET":
    return 'Hello Kognita'

@app.route('/get_data/<author_name>', methods=['GET'])
def get_data(author_name):
    # try query the data structure
    # except no data return
    print(type(author_name))
    print(author_name)
    data = get_author_question(author_name, result_data_scraper_selenium)

    if data is not None:
        response = jsonify(data), 200
    else:
        response = {"data": "No data for that user"}, 404
    return response


def get_author_question(author_name, data):
    results = []
    for i, row in enumerate(data):
        if author_name == row['question']['question_author_name']:
            results.append(data[i])
    if len(results) > 0:
        print(f'This user make {len(results)} questions')
        for question in results:
            print(question)
        return results
    else:
        return None


