import os
import unittest

from flask_migrate import Migrate

from app import blueprint
from app.main import create_app, db
from app.main.model import user, blacklist, category
from dotenv import load_dotenv

load_dotenv()
app = create_app(os.getenv('FLASK_ENV') or 'development')
app.register_blueprint(blueprint)

app.app_context().push()

migrate = Migrate(app, db)


def run_app():
     app.run()

def testing():
    """Runs the unit tests."""
    tests = unittest.TestLoader().discover('app/test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

if __name__ == '__main__':
     print('environment' + os.getenv('FLASK_ENV'))
     run_app()