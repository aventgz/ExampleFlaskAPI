import time
import json
import random
import math
import traceback
import uuid
from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from typing import Dict, List
from ExampleFlaskAPI.database_bridge import DatabaseBridge
from ExampleFlaskAPI.authorization import Authorization
from ExampleFlaskAPI.api import API

# Custom MongoDB URI
MONGODB_URI: str = 'mongodb+srv://<nickname>:<password>@<server_ip>/<database_name>?retryWrites=true&w=majority'

# Example list of 50 parts
example_industrial_communication_elements: Dict[str, str] = {
    "PLC module": "Controls industrial processes with programmable logic.",
    "Industrial controller": "Manages automation tasks in industrial settings.",
    "HMI user interface": "Allows interaction between humans and machines.",
    "Industrial switch": "Connects devices in industrial Ethernet networks.",
    "Industrial router": "Routes data between different industrial networks.",
    "I/O module": "Manages input and output signals in automation systems.",
    "Data concentrator": "Aggregates and forwards data in industrial networks.",
    "Protocol converter": "Translates data between different communication protocols.",
    "Network bridge": "Connects two different network segments.",
    "Signal amplifier": "Boosts signals for long-distance transmission.",
    "Industrial terminal": "Provides interface for data input and output.",
    "Industrial transceiver": "Transmits and receives data in industrial environments.",
    "Operator panel": "Allows operators to monitor and control processes.",
    "Industrial gateway": "Connects different industrial networks together.",
    "Network adapter": "Enables devices to connect to industrial networks.",
    "Motion controller": "Controls the movement of motors and actuators.",
    "Industrial network card": "Provides network connectivity to industrial devices.",
    "Safety controller": "Ensures safety in industrial automation systems.",
    "Communication module": "Facilitates communication between devices.",
    "Process visualization system": "Visualizes processes for monitoring and control.",
    "Motor controller": "Regulates speed and direction of motors.",
    "Industrial communication protocol": "Specifies rules for data exchange in industries.",
    "Industrial Ethernet switch": "Manages data transmission in Ethernet networks.",
    "Industrial modem": "Connects industrial devices over telephone lines.",
    "Industrial OPC server": "Provides data exchange between different systems.",
    "MODBUS protocol": "Standard for communication between industrial devices.",
    "RS-232/RS-485 interface": "Common serial interfaces for industrial devices.",
    "Industrial computer": "Designed for harsh industrial environments.",
    "Industrial buzzer": "Produces audible alerts in industrial settings.",
    "Industrial antenna": "Facilitates wireless communication in industries.",
    "Temperature controller": "Regulates temperature in industrial processes.",
    "Communication barriers": "Ensures isolation between different networks.",
    "Signal converter": "Converts signals between analog and digital formats.",
    "Industrial networking support": "Provides networking assistance for industries.",
    "Industrial repeater": "Boosts and retransmits signals in networks.",
    "SCADA system": "Supervisory Control and Data Acquisition system for industries.",
    "Industrial sensor": "Measures physical properties in industrial processes.",
    "Industrial USB interface": "Enables USB connectivity in industrial devices.",
    "Industrial data transmitter": "Transmits data wirelessly in industrial environments.",
    "Process monitoring and control": "Oversees and regulates industrial processes.",
    "Cable support": "Provides support for cables in industrial installations.",
    "LED display module": "Displays information using LED technology.",
    "Industrial diagnostics system": "Diagnoses faults in industrial equipment.",
    "Energy management system": "Optimizes energy usage in industrial facilities.",
    "Industrial splitter": "Splits data signals into multiple streams.",
    "Quality control system": "Ensures products meet specified standards.",
    "Network concentrator": "Aggregates data from multiple network devices.",
    "Industrial wireless system": "Enables wireless communication in industries.",
    "Industrial Ethernet interface": "Connects devices to Ethernet networks.",
    "Industrial protocol converter": "Converts between different industrial protocols."
}

def input_random_data(mongo: DatabaseBridge, category_count: int = 2, part_count: int = 20) -> None:
    """
    Generate and insert random data into database

    Args:
        mongo (DatabaseBridge): Database bridge
        category_count (int): Number of categories to add
        part_count (int): Number of parts to add       
    """

    if all(collection in mongo.get_collection_names() for collection in ['Item', 'Category']):
        return

    category_count = 2 if category_count < 2 else category_count
    part_count = 20 if part_count < 20 else part_count

    max_locations_count: int = math.ceil(part_count * 0.1)

    categories: List[str] = ['Category_' + str(i) for i in range(1, category_count + 1)]

    category_rows: List[str] = [{'name': str(i), 'parent_name': ''} for i in categories]

    part_rows: List[Dict] = [
        {
            'serial_number': str(uuid.uuid4()),
            'name': info,
            'description': example_industrial_communication_elements[info],
            'category': random.choice(categories),
            'price': round(random.uniform(1, 10), 2),
            'location': {
                'room': random.randint(1, max_locations_count),
                'bookcase': random.randint(1, max_locations_count),
                'shelf': random.randint(1, max_locations_count),
                'cuvette': random.randint(1, max_locations_count),
                'column': random.randint(1, max_locations_count),
                'row': random.randint(1, max_locations_count)
            }
        } 
        
        for i in range(1, part_count + 1)
        for info in [random.choice(list(example_industrial_communication_elements.keys()))]
    ]

    # Add rows to mongodb
    mongo.insert_many('Category', category_rows)
    mongo.insert_many('Item', part_rows)

def main():  
    # Initialize Flask app
    app: any = Flask(__name__)

    # Provide mongodb URI
    app.config['MONGO_URI'] = MONGODB_URI
    
    # Create database client
    client: PyMongo = PyMongo(app)

    # Create mongo bridge
    mongo: DatabaseBridge = DatabaseBridge(client)

    authorization: Authorization = Authorization()

    # Create example sessions with assigned permissions
    authorization.create_session('example_read', ['READ'])
    authorization.create_session('example_create', ['CREATE'])
    authorization.create_session('example_update', ['UPDATE'])
    authorization.create_session('example_delete', ['DELETE'])
    authorization.create_session('example_all', ['READ', 'CREATE', 'UPDATE', 'DELETE']) 

    # Initialize API object
    API(app, mongo, authorization)
    
    input_random_data(mongo)

    # Run app
    app.run(debug=True)