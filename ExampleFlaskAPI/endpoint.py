import time
import json
import werkzeug
import traceback
from typing import Callable, Dict, Union, List, TypedDict, Tuple
from flask import Flask, jsonify, request
from ExampleFlaskAPI.utils import StructureDict, Utils
from ExampleFlaskAPI.database_bridge import DatabaseBridge
from ExampleFlaskAPI.authorization import Authorization

class Endpoint: 
    """
    Base class for handling requests

    Attributes:
        _mongo (DatabaseBridge): Bridge to mongodb
        _codes (Dict[int, Dict[str, str]]): List of internal server messages    
        _authorization (Authorization): Inteface for user authorization
        __http_status_codes (Dict[int, str]): List of HTTP codes
    """       

    def _route(self, **kwargs) -> str:
        """
        Initialize authorization and forward request

        Args:
            **kwargs: arguments passed by Flask

        Returns:
            str: Return server response
        """

        # Setup default language
        language: str = 'en-EN'
        
        # Authorize user
        if not self._authorization.is_authorized(request, request.method):
            return self.__response(language, 401, False, 0)
        
        try:
            # Check for best fitting language
            language = request.accept_languages.best
            
            # Hook default method
            method_hook: Callable = self._NOT_ALLOWED

            # Hook requested method
            if request.method == 'GET':
               method_hook = self._GET
            elif request.method == 'HEAD':
                method_hook = self._HEAD  
            elif request.method == 'POST':
                method_hook = self._POST
            elif request.method == 'PUT':
                method_hook = self._PUT        
            elif request.method == 'PATCH':
                method_hook = self._PATCH
            elif request.method == 'DELETE':
                method_hook = self._DELETE
            else:
                return self.__response(language, 405, False, 0)
            
            # Process request
            response: int; success: bool; code: int; result: List

            response, success, code, result, *_ = method_hook(request, **kwargs) + ([],) * 4
                      
            return self.__response(language, response, success, code, result)
        except Exception as e:
            traceback.print_exc() 
            return self.__response(language, 500, False, 0)
                      
    def _GET(self, request: werkzeug.local.LocalProxy, **kwargs) -> Tuple[int, bool, int, List]:
        """
        Template for GET method

        Args:
            request (werkzeug.local.LocalProxy): Flask request
            **kwargs: arguments passed by Flask

        Returns:
            Tuple[int, bool, int, List]: Return response
        """      

        # Return not found error
        return 404, False, 0       
    
    def _HEAD(self, request: werkzeug.local.LocalProxy, **kwargs) -> Tuple[int, bool, int, List]:
        """
        Template for HEAD method

        Args:
            request (werkzeug.local.LocalProxy): Flask request
            **kwargs: arguments passed by Flask

        Returns:
            Tuple[int, bool, int, List]: Return response
        """   

        # Return not found error
        return 404, False, 0    
        
    def _POST(self, request: werkzeug.local.LocalProxy, **kwargs) -> Tuple[int, bool, int, List]:
        """
        Template for POST method

        Args:
            request (werkzeug.local.LocalProxy): Flask request
            **kwargs: arguments passed by Flask

        Returns:
            Tuple[int, bool, int, List]: Return response
        """   
       
        # Return not found error
        return 404, False, 0    
        
    def _PUT(self, request: werkzeug.local.LocalProxy, **kwargs) -> Tuple[int, bool, int, List]:
        """
        Template for PUT method

        Args:
            request (werkzeug.local.LocalProxy): Flask request
            **kwargs: arguments passed by Flask

        Returns:
            Tuple[int, bool, int, List]: Return response
        """   


        # Return not found error
        return 404, False, 0
        
    def _PATCH(self, request: werkzeug.local.LocalProxy, **kwargs) -> Tuple[int, bool, int, List]:
        """
        Template for PATCH method

        Args:
            request (werkzeug.local.LocalProxy): Flask request
            **kwargs: arguments passed by Flask

        Returns:
            Tuple[int, bool, int, List]: Return response
        """   
       
        # Return not found error
        return 404, False, 0
        
    def _DELETE(self, request: werkzeug.local.LocalProxy, **kwargs) -> Tuple[int, bool, int, List]:
        """
        Template for DELETE method

        Args:
            request (werkzeug.local.LocalProxy): Flask request
            **kwargs: arguments passed by Flask

        Returns:
            Tuple[int, bool, int, List]: Return response
        """   

        # Return not found error
        return 404, False, 0
      
    def _NOT_ALLOWED(self, request: werkzeug.local.LocalProxy, **kwargs) -> Tuple[int, bool, int, List]:
        """
        Template for NOT ALLOWED method

        Args:
            request (werkzeug.local.LocalProxy): Flask request
            **kwargs: arguments passed by Flask

        Returns:
            Tuple[int, bool, int, List]: Return response
        """   
       
        # Return not allowed error
        return 405, False, 0
   
    def __response(self, language: str, response: int, success: bool, code: int, result: List = []) -> str:
        """
        Build final server response

        Args:
            language (str): Client language
            response (int): Internal response code
            success (bool): Success state
            code (int): HTTP code
            result (List): Results of operation

        Returns:
            str: Return created final server response
        """   

        # Check if HTTP status code exist
        if response not in self.__http_status_codes:
            raise ValueError("Wrong HTTP response status.")
        
        code: int; message: str

        code, message = self.__status(language, code)                    
         
        return json.dumps({
            'response': {
                'code': response,
                'status': self.__http_status_codes[response]
            }, 
            'status': {
                'success': success,
                'code': code, 
                'message': message
            }, 
            'timestamp': int(time.time()), 
            'result': result
        }, default=str), response, {'Content-Type': 'text/html; charset=utf-8'}
        
    def __status(self, language: str, code: int) -> Tuple[int, str]:
        """
        Return status message in prefered language

        Args:
            language (str): Client language
            code (int): Internal server response code

        Returns:
            Tuple[int, str]: Return internal server response code and message
        """  

        try:           
            # Check for code and language inside codes
            if code not in self._codes:
                return code, ''
                
            if language in self._codes[code]:
                return code, self._codes[code][language] 
            elif 'en-EN' in self._codes[code]:
                return code, self._codes[code]['en-EN']

            return code, ''
        except Exception as e:
            traceback.print_exc() 
            return 0, ''
            
    @staticmethod
    def required_structure(structure: StructureDict) -> Tuple[int, bool, int, List]:
        """
        Check for required data input structure

        Args:
            structure (StructureDict): Required structure of input data

        Returns:
            Tuple[int, bool, int, List]: Return internal server response from function
        """  

        def decorator(func):
            def wrapper(*args, **kwargs):
                try:
                    # Get input data
                    data: List[Dict] = args[1].get_json()

                    # Check data structure
                    if not isinstance(data, list) or not Utils.check_structure(data, structure):
                        return 400, False, 0, {'message': 'Bad structure.', 'required_structure': structure}               
                    
                    return func(*args, **kwargs)
                except Exception as e:
                    traceback.print_exc() 
                    return 500, False, 0              
            return wrapper
        return decorator      

    def __init__(self, mongo: DatabaseBridge, codes: Dict[int, Dict[str, str]], authorization: Authorization):   
        """
        Initialize default Endpoint

        Args:
            mongo (DatabaseBridge): Assign mongodb bridge
            codes (Dict[int, Dict[str, str]]): Assign internal server messages
            authorization (Authorization): Assign authorization class
        """          

        self._mongo: DatabaseBridge = mongo
        self._codes: Dict[int, Dict[str, str]] = codes      
        self._authorization: Authorization = authorization
        
        # HTTP status codes
        self.__http_status_codes: Dict[int, str] = {
            100: 'Continue',
            101: 'Switching Protocols',
            102: 'Processing',
            103: 'Early Hints',
            200: 'OK',
            201: 'Created',
            202: 'Accepted',
            203: 'Non-Authoritative Information',
            204: 'No Content',
            205: 'Reset Content',
            206: 'Partial Content',
            207: 'Multi-Status',
            208: 'Already Reported',
            226: 'IM Used',
            300: 'Multiple Choices',
            301: 'Moved Permanently',
            302: 'Found',
            303: 'See Other',
            304: 'Not Modified',
            305: 'Use Proxy',
            306: 'Switch Proxy',
            307: 'Temporary Redirect',
            308: 'Permanent Redirect',
            400: 'Bad Request',
            401: 'Unauthorized',
            402: 'Payment Required',
            403: 'Forbidden',
            404: 'Not Found',
            405: 'Method Not Allowed',
            406: 'Not Acceptable',
            407: 'Proxy Authentication Required',
            408: 'Request Timeout',
            409: 'Conflict',
            410: 'Gone',
            411: 'Length Required',
            412: 'Precondition Failed',
            413: 'Payload Too Large',
            414: 'URI Too Long',
            415: 'Unsupported Media Type',
            416: 'Range Not Satisfiable',
            417: 'Expectation Failed',
            418: "I'm a teapot",
            421: 'Misdirected Request',
            422: 'Unprocessable Entity',
            423: 'Locked',
            424: 'Failed Dependency',
            425: 'Too Early',
            426: 'Upgrade Required',
            428: 'Precondition Required',
            429: 'Too Many Requests',
            431: 'Request Header Fields Too Large',
            451: 'Unavailable For Legal Reasons',
            500: 'Internal Server Error',
            501: 'Not Implemented',
            502: 'Bad Gateway',
            503: 'Service Unavailable',
            504: 'Gateway Timeout',
            505: 'HTTP Version Not Supported',
            506: 'Variant Also Negotiates',
            507: 'Insufficient Storage',
            508: 'Loop Detected',
            510: 'Not Extended',
            511: 'Network Authentication Required'
        }

class OperationStatusDict(TypedDict):
    """
    Operation status response structure
    """

    id: str
    status: bool
    message: str