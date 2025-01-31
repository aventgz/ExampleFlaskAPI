import pytest
import pymongo
from flask_pymongo import PyMongo
from flask import Flask, jsonify, request
from typing import List, Dict
from ExampleFlaskAPI.database_bridge import DatabaseBridge
from ExampleFlaskAPI.authorization import Authorization

def test_create_session():
    """Test creating a session with correct permissions"""

    authorization: Authorization = Authorization()

    assert authorization.create_session('test', ['WRONG_PERMISSION', 'READ']) == False
    assert authorization.create_session('test', ['READ']) == True
    assert authorization.create_session('test', ['Write']) == False # Recreating already created session id

def test_is_authorized():
    """Test for checking method authorization"""

    authorization: Authorization = Authorization() 
    authorization.create_session('test', ['READ']) # Create example session with GET method permission

    app = Flask(__name__)

    with app.test_request_context(
    '/test', # URL path
    headers={'Authorization': 'test'} # Headers
    ) as context:
        assert authorization.is_authorized(request, 'GET') ==  True
        assert authorization.is_authorized(request, 'DELETE') ==  False