from flask import Flask
from flask import jsonify


app = Flask(__name__)

app.route('/<user_name>', methods=['GET'])
def provide_data(user_name):
    # try query the data structure
    # except no data return
    try:
        data = user_name
        response = jsonify(data), 200
    except Exception as error:
        response = error, 404

    return response






