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

@pytest.fixture
def setup():
    """Fixture setup database bridge"""

    app = Flask(__name__)

    app.config["MONGO_URI"] = "mongodb://testdb"  
    app.config["TESTING"] = True 
    mongo = PyMongo(app)
        
    # Use a fresh mongomock client for each test
    mongo.cx = mongomock.MongoClient()
    mongo.db = mongo.cx["testdb"]
        
    database_bridge = DatabaseBridge(mongo)

    yield database_bridge, mongo

def test_find(setup):
    """Test database finding"""

    database_bridge, mongo = setup

    mongo.db['Category'].insert_one({'name': 'test', 'parent_name': ''})
    mongo.db['Category'].insert_one({'name': 'test1', 'parent_name': ''})

    assert len(database_bridge.find('Category', {}, limit=1)) == 1
    assert len(database_bridge.find('Category', {})) == 2
    assert database_bridge.find('Category', {'name': 'test'})[0]['name'] == 'test'

def test_find_one(setup):
    """Test database single object finding"""

    database_bridge, mongo = setup
    
    mongo.db['Category'].insert_one({'name': 'test', 'parent_name': ''})
    mongo.db['Category'].insert_one({'name': 'test1', 'parent_name': ''})

    assert database_bridge.find_one('Category', {'name': 'test'})['name'] == 'test'

def test_insert_one(setup):
    """Test database insertion for a single row"""

    database_bridge, mongo = setup

    database_bridge.insert_one('Category', {'name': 'test', 'parent_name': ''})
    
    assert mongo.db['Category'].find_one({'name': 'test'})['name'] == 'test'   

def test_insert_many(setup):
    """Test inserting multiple rows into the database"""

    database_bridge, mongo = setup

    database_bridge.insert_many('Category', [{'name': 'test', 'parent_name': ''}, {'name': 'test1', 'parent_name': ''}])

    assert len(database_bridge.find('Category', {})) == 2   

def test_delete_many(setup):
    """Test deleting multiple rows from database"""

    database_bridge, mongo = setup
    
    mongo.db['Category'].insert_one({'name': 'test', 'parent_name': ''})

    database_bridge.delete_many('Category', {'name': 'test'})

    assert mongo.db['Category'].find_one({'name': 'test'}) == None

def test_update_one(setup):
    """Test updating single row in database"""

    database_bridge, mongo = setup
    
    mongo.db['Category'].insert_one({'name': 'test', 'parent_name': ''})
    mongo.db['Category'].insert_one({'name': 'test1', 'parent_name': ''})

    database_bridge.update_one('Category', {'name': 'test'}, {'$set': {'parent_name': 'test1'}})

    assert mongo.db['Category'].find_one({'name': 'test'})['parent_name'] == 'test1'

def test_update(setup):
    """Test updating many rows in database"""

    database_bridge, mongo = setup
    
    mongo.db['Category'].insert_one({'name': 'test', 'parent_name': ''})
    mongo.db['Category'].insert_one({'name': 'test1', 'parent_name': ''})
    mongo.db['Category'].insert_one({'name': 'test2', 'parent_name': ''})

    database_bridge.update_many('Category', {'name': {'$in': ['test', 'test1']}}, {'$set': {'parent_name': 'test2'}})

    assert mongo.db['Category'].find_one({'name': 'test1'})['parent_name'] == 'test2' 

def test_get_collection_names(setup):
    """Test getting collection names from database"""

    database_bridge, mongo = setup
    
    mongo.db['Category'].insert_one({'name': 'test', 'parent_name': ''})

    assert database_bridge.get_collection_names() == ['Category'] 
