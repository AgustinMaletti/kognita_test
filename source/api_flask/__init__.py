from flask import Flask


def create_app(file_name:str):
    '''
    Defines creation of app object and passing config  parameters
    :param file_name is hte absolute path to the data json file

    '''
    app = Flask(__name__)
    app.config['file_name'] = file_name
    from source.api_flask.app import main
    from source.api_flask.errors_handlers.error_handlers import errors
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app