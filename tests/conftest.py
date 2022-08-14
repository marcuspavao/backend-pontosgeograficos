import pytest
import os, sys
p = os.path.abspath('..')
a = os.path.abspath('.')
sys.path.insert(1, p)
sys.path.insert(1, a)

from main import app, mongo_connection

@pytest.fixture(scope="module")
def apps():
    return app

@pytest.fixture(scope="module")
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture(scope="module")
def db():
    """Mongo DB"""
    return mongo_connection()


