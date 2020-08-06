from unittest import TestCase
from source.api_flask import create_app
from source.config import DIR_DATA
import io
import sys

FILE_FOR_API = DIR_DATA.joinpath('data3.json')

class Test_Api(TestCase):

    def create_app(self):
        app = create_app(file_name=FILE_FOR_API)
        app.config['TESTING'] = True
        app.config['DEBUG'] = True
        app.config['LIVESERVER_PORT'] = 8000,
        app.config['LIVESERVER_TIMEOUT'] = 10,
        app.config['file_name'] = FILE_FOR_API
        self.app_context = app.app_context()
        self.app_context.push()
        return app

    def setUp(self):
        self.app = self.create_app()
        self.client = self.app.test_client()

    def tearDown(self):
        self.app_context.pop()

    def test_author_list_200(self):
        response = self.client.get('/user_list')
        self.assertEqual(response.status_code, 200)

    def test_author_list_key_is_present(self):
        response = self.client.get('/user_list')
        self.assertIn('author_list', response.get_json())

    def test_author_list_author_is_present(self):
        response = self.client.get('/user_list')
        self.assertIn('CCCCos', response.get_json()['author_list'])

    def test_author_data_is_not_present(self):
        response = self.client.get('/get_data/agustin')
        self.assertIn('No data for that user', response.get_json()['data'])

    def test_author_data_is_present(self):
        response = self.client.get('/get_data/victorcd')
        question_part = 'I have model where I can upload files without problem, and a model forms which upload'
        self.assertIn(question_part, response.get_json()[0]['question']['question_text'])




def print_in_test(hello):
    ''' Capture print statement in test '''
    captured_output = io.StringIO()                  # Create StringIO object
    sys.stdout = captured_output                     #  and redirect stdout.
    print(hello)                                     # Call unchanged function.
    sys.stdout = sys.__stdout__                      # Reset redirect.
    print('Captured', captured_output.getvalue())