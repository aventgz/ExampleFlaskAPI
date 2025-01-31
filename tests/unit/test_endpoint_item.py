import pytest
import mongomock
import pymongo
from flask_pymongo import PyMongo
from flask import Flask, jsonify, request
from unittest import mock
from typing import List, Dict
from ExampleFlaskAPI.database_bridge import DatabaseBridge
from ExampleFlaskAPI.endpoint_item import EndpointItem
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
    """Test getting item"""

    database_bridge, mongo, app = setup

    database_bridge.insert_one('Item', 
        {'serial_number': 'test',
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

    endpoint: EndpointItem = EndpointItem(database_bridge, [], Authorization())

    with app.test_request_context(
    '/api/v1/item/test', # URL path
    method='GET', # HTTP method
    ) as context:
        assert endpoint._GET(request, 'test')[3][0]['serial_number'] == 'test'
        assert endpoint._GET(request, 'test1')[3] == []

def test_post(setup):
    """Test inserting item"""

    database_bridge, mongo, app = setup

    endpoint: EndpointItem = EndpointItem(database_bridge, [], Authorization())

    with app.test_request_context(
    '/api/v1/item', # URL path
    method='POST', # HTTP method
    json=[{'serial_number': 'test',
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
         }] # JSON payload
    ) as context:      
        result: List = endpoint._POST(request)[3]
        
        assert result[0]['id'] == 'test'
        assert result[0]['status'] == True
        
        del request.json[0]['_id']
        result = endpoint._POST(request)[3]

        assert result[0]['id'] == 'test'
        assert result[0]['status'] == False  
        
def test_put(setup):
    """Test updating item"""

    database_bridge, mongo, app = setup

    endpoint: EndpointItem = EndpointItem(database_bridge, [], Authorization())

    with app.test_request_context(
    '/api/v1/item', # URL path
    method='PUT', # HTTP method
    json=[{'serial_number': 'test',
            'change':{
                'name': 'test_name1',
                'description': 'test_description1',
                'category': 'test_category',
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
         }] # JSON payload
    ) as context:      
        result: List = endpoint._PUT(request)[3]

        assert result[0]['id'] == 'test'
        assert result[0]['status'] == False
            
        database_bridge.insert_one('Category', {'name': 'test_category', 'parent_name': ''})    
        database_bridge.insert_one('Item', {'serial_number': 'test',
            'change': {
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
        })

        result = endpoint._PUT(request)[3]

        assert result[0]['id'] == 'test'
        assert result[0]['status'] == True

def test_patch(setup):
    """Test updating item"""

    database_bridge, mongo, app = setup

    endpoint: EndpointItem = EndpointItem(database_bridge, [], Authorization())

    with app.test_request_context(
    '/api/v1/item', # URL path
    method='PATCH', # HTTP method
    json=[{'serial_number': 'test',
            'change':{
                'category': 'test_category',
                'price': 1.3,
                'location': {
                    'column': 2,
                    'row': 1
                }
            }
         }] # JSON payload
    ) as context:      
        result: List = endpoint._PATCH(request)[3]

        assert result[0]['id'] == 'test'
        assert result[0]['status'] == False
            
        database_bridge.insert_one('Category', {'name': 'test_category', 'parent_name': ''})    
        database_bridge.insert_one('Item', {'serial_number': 'test',
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
        })

        result = endpoint._PATCH(request)[3]

        assert result[0]['id'] == 'test'
        assert result[0]['status'] == True

def test_delete(setup):
    """Test deleting item"""

    database_bridge, mongo, app = setup

    endpoint: EndpointItem = EndpointItem(database_bridge, [], Authorization())

    with app.test_request_context(
    '/api/v1/item/test', # URL path
    method='DELETE', # HTTP method
    ) as context:      
        result: List = endpoint._DELETE(request, 'test')[3]
        assert result[0]['status'] == False
            
        database_bridge.insert_one('Item', {'serial_number': 'test',
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
        })

        result = endpoint._DELETE(request, 'test')[3]

        assert result[0]['status']== True
