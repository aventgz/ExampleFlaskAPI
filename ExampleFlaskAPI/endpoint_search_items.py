import werkzeug
import traceback
from flask import Flask, jsonify, request
from typing import List, Dict, Tuple
from ExampleFlaskAPI.endpoint import Endpoint

class EndpointSearchItems(Endpoint):
    """
    A child class to handle item search requests
    """   

    def route_search_items(self, **kwargs) -> str:
        """
        Forwarding to the main routing function

        Args:
            **kwargs: arguments passed by Flask

        Returns:
            str: Return server response
        """

        return self._route(**kwargs)

    def _GET(self, request: werkzeug.local.LocalProxy) -> Tuple[int, bool, int, List]:
        """
        Implementation of GET method to search items

        Args:
            request (werkzeug.local.LocalProxy): Flask request

        Returns:
            Tuple[int, bool, int, List]: Return response
        """   

        collection_name: str = ''
        query: Dict = {}
         
        collection_name, query = self.__GET_items(request)

        if len(collection_name) <= 0:
            return 400, False, 1406, []

        skip: int = 0
        limit: int = -1

        skip_value: str = request.args.get('skip')
        limit_value: str = request.args.get('limit')

        if skip_value:
            skip = int(float(skip_value))
        if limit_value:
            limit = int(float(limit_value))            

        return 200, True, 1200, list(self._mongo.find(collection_name, query, skip, limit))

    def __GET_items(self, request: werkzeug.local.LocalProxy) -> Tuple [str, Dict]:
        """
        Implementation of GET method to search items

        Args:
            request (werkzeug.local.LocalProxy): Flask request

        Returns:
            Tuple[str, Dict]: Return collection name and query
        """   

        query: Dict = {}

        # Create conditions
        self.__split_values_list(query, 'serial_number', request, False, str)
        self.__split_values_list(query, 'name', request, False, str)
        self.__split_values_list(query, 'category', request, False, str)   
        self.__split_values_list(query, 'price', request, True, float)     
        self.__split_values_list(query, 'location_room', request, True, int)
        self.__split_values_list(query, 'location_bookcase', request, True, int)
        self.__split_values_list(query, 'location_shelf', request, True, int)
        self.__split_values_list(query, 'location_cuvette', request, True, int)
        self.__split_values_list(query, 'location_column', request, True, int)
        self.__split_values_list(query, 'location_row', request, True, int)

        return 'Item', query

    def __split_values_list(self, query: Dict, name: str, values: request, range: bool, value_type: type) -> None:
        """
        Split values to achive list for query condition

        Args:
            query (Dict): Pointer to query conditions container
            name (str): Name of attribute
            values (request.args): Request parameters
            value_type (type): Type to which each value should be converted
        """

        allowed_types: list[type] = [str, int, float]
        
        if value_type not in allowed_types:
            return None

        try:
            if range:
                # Check for min/max values
                min: value_type = values.args.get('min_' + name, type=str)
                max: value_type = values.args.get('max_' + name, type=str)

                temp_query: query = {}

                # Create MongoDB query           
                if min:
                    temp_query["$gte"] = value_type(float(min))
                if max:
                    temp_query["$lte"] = value_type(float(max))

                if len(temp_query) > 0:
                    query[name.replace("_", ".")] = temp_query    
                    return

            direct: str = values.args.get(name, type=str)

            if direct:
                query[name.replace("_", ".")] = {"$in": [value_type(v.strip()) for v in direct.split(',')]}
                
            return None
        except:
            traceback.print_exc()
            return      