from dotenv import load_dotenv
from datetime import timedelta
from pathlib import Path
from src.custom_filters import CUSTOM_FILTERS
from importlib import import_module
from flask import Flask
import logging


load_dotenv()

application = Flask(__name__)
application.logger.handlers = []
application.logger.addHandler(logging.StreamHandler())
application.jinja_env.filters.update(CUSTOM_FILTERS)

get_name = lambda x: str(x).split('/')[-1].replace('.py', '')

# initialize dynamodb tables and models
models = Path('./src/models')
for model in models.iterdir():
    if model.is_file() and get_name(model) != 'base':
        logging.info(f'initiating dynamodb table for {model}')
        import_module(f'src.models.{get_name(model)}').init()

# register blueprints for all views
views = Path('./views')
for view in views.iterdir():
    if view.is_file():
        application.register_blueprint(
            import_module(f'views.{get_name(view)}').routes
        )


if __name__ == '__main__':
    application.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
