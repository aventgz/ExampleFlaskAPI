import pytest
import werkzeug
import mongomock
import flask
import pymongo
from flask_pymongo import PyMongo
from flask import Flask, jsonify, request
from unittest import mock
from typing import List, Dict, Tuple
from ExampleFlaskAPI.endpoint import Endpoint
from ExampleFlaskAPI.endpoint_search_items import EndpointSearchItems
from ExampleFlaskAPI.database_bridge import DatabaseBridge
from ExampleFlaskAPI.authorization import Authorization

class DatabaseBridgeTest(DatabaseBridge):
    class start_session():
        class start_transaction():
            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc_value, traceback):
                pass                       

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            pass  

@pytest.fixture
def setup():
    """Fixture setup database bridge"""

    app = Flask(__name__)

    app.config["MONGO_URI"] = "mongodb://testdb"  
    app.config["TESTING"] = True 
    mongo = PyMongo(app)
        
    # Use a new mongomock client for each test case
    mongo.cx = mongomock.MongoClient()
    mongo.db = mongo.cx["testdb"]
        
    database_bridge = DatabaseBridgeTest(mongo)

    yield database_bridge, mongo, app

def test_get(setup):
    """Test getting items"""

    database_bridge, mongo, app = setup

    database_bridge.insert_one('Item', 
        {'serial_number': 'test1',
            'name': 'test_name',
            'description': 'test_description',
            'category': '',
            'price': 1.0,
            'location': {
                'room': 1,
                'bookcase': 1,
                'shelf': 1,
                'cuvette': 1,
                'column': 1,
                'row': 1
            }
        }
    )
    database_bridge.insert_one('Item', 
        {'serial_number': 'test2',
            'name': 'test_name',
            'description': 'test_description',
            'category': '',
            'price': 2.0,
            'location': {
                'room': 1,
                'bookcase': 2,
                'shelf': 1,
                'cuvette': 1,
                'column': 1,
                'row': 1
            }
        }
    )
    database_bridge.insert_one('Item', 
        {'serial_number': 'test3',
            'name': 'test_name',
            'description': 'test_description',
            'category': '',
            'price': 3.0,
            'location': {
                'room': 1,
                'bookcase': 3,
                'shelf': 1,
                'cuvette': 1,
                'column': 1,
                'row': 1
            }
        }
    )         

    endpoint: EndpointSearchItems = EndpointSearchItems(database_bridge, [], Authorization())

    with app.test_request_context(
    '/api/v1/search/items?min_price=2&location_bookcase=3', # URL path
    method='GET', # HTTP method
    ) as context:
        assert endpoint._GET(request)[3][0]['serial_number'] == 'test3'
        