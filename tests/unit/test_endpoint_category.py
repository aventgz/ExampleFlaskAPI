import pytest
import mongomock
import pymongo
from flask_pymongo import PyMongo
from flask import Flask, jsonify, request
from unittest import mock
from typing import List, Dict
from ExampleFlaskAPI.database_bridge import DatabaseBridge
from ExampleFlaskAPI.endpoint_category import EndpointCategory
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
    """Test getting category"""

    database_bridge, mongo, app = setup

    database_bridge.insert_one('Category', {'name': 'test', 'parent_name': ''})
    
    endpoint: EndpointCategory = EndpointCategory(database_bridge, [], Authorization())

    with app.test_request_context(
    '/api/v1/category/test', # URL path
    method='GET', # HTTP method
    ) as context:
        assert endpoint._GET(request, 'test')[3][0]['name'] == 'test'

def test_post(setup):
    """Test inserting category"""

    database_bridge, mongo, app = setup

    endpoint: EndpointCategory = EndpointCategory(database_bridge, [], Authorization())

    with app.test_request_context(
    '/api/v1/category', # URL path
    method='POST', # HTTP method
    json=[{'name': 'test', 'parent_name': ''}] # JSON payload
    ) as context:    
        result: List = endpoint._POST(request)[3]

        assert result[0]['id'] == 'test'
        assert result[0]['status'] == True
        
        del request.json[0]['_id']
        result = endpoint._POST(request)[3]

        assert result[0]['id'] == 'test'
        assert result[0]['status'] == False  

def test_put(setup):
    """Test updating category"""

    database_bridge, mongo, app = setup

    endpoint: EndpointCategory = EndpointCategory(database_bridge, [], Authorization())

    with app.test_request_context(
    '/api/v1/category', # URL path
    method='PUT', # HTTP method
    json=[{'name': 'test', 'change': {'parent_name': ''}}] # JSON payload
    ) as context:      
        result: List = endpoint._PUT(request)[3]

        assert result[0]['id'] == 'test'
        assert result[0]['status'] == False
            
        database_bridge.insert_one('Category', {'name': 'test', 'parent_name': 'test1'})

        result = endpoint._PUT(request)[3]

        assert result[0]['id'] == 'test'
        assert result[0]['status'] == True

def test_patch(setup):
    """Test updating category"""

    database_bridge, mongo, app = setup

    endpoint: EndpointCategory = EndpointCategory(database_bridge, [], Authorization())

    with app.test_request_context(
    '/api/v1/category', # URL path
    method='PATCH', # HTTP method
    json=[{'name': 'test', 'change': {}}] # JSON payload
    ) as context:      
        result: List = endpoint._PATCH(request)[3]

        assert result[0]['id'] == 'test'
        assert result[0]['status'] == False
            
        database_bridge.insert_one('Category', {'name': 'test', 'parent_name': ''})

        result = endpoint._PATCH(request)[3]

        assert result[0]['id'] == 'test'
        assert result[0]['message'] == 'No modifications were made.'

def test_delete(setup):
    """Test deleting category"""

    database_bridge, mongo, app = setup

    endpoint: EndpointCategory = EndpointCategory(database_bridge, [], Authorization())

    with app.test_request_context(
    '/api/v1/category/test', # URL path
    method='DELETE', # HTTP method
    ) as context:      
        result: List = endpoint._DELETE(request, 'test')[3]

        assert result[0]['id'] == 'test'
        assert result[0]['status'] == False
            
        database_bridge.insert_one('Category', {'name': 'test', 'parent_name': ''})

        result = endpoint._DELETE(request, 'test')[3]
        
        assert result[0]['id'] == 'test'
        assert result[0]['status'] == True                              