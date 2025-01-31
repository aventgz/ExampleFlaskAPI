import time
import werkzeug
import traceback
from typing import List, Dict

class Authorization: 
    """
    User authorization class

    Attributes:
        __permissions (Dict[str, List[str]]): List of all permissions
        __sessions (Dict): Created sessions with assigned permissions
    """   

    def is_authorized(self, request: werkzeug.local.LocalProxy, method: str) -> bool:
        """
        Check if provided key is correct and authorized for action

        Args:
            request (werkzeug.local.LocalProxy): Flask request
            method (str): Requested action
      
        Returns:
            bool: Return true if authorized
        """

        # Obtain Authentication header
        key: str = request.headers.get('Authorization')
        
        # Check if exists, if not check for api_key in args
        if not key:
            key = request.args.get('api_key', type=str)

        # If not provided any key, return False
        if not key or key not in self.__sessions:
            return False
           
        # Validate permissions
        return any(method in self.__permissions[permission] for permission in self.__sessions[key]["permissions"])
        
    def create_session(self, key: str, permissions: List[str]) -> bool:
        """
        Create session with provided key and permissions

        Args:
            key (str): Key to authorize
            permissions (List[str]): Permission available by key
      
        Returns:
            bool: Return true if created
        """

        key: str = str(key)
        
        # Check for existence of key and permissions
        if key in self.__sessions or not isinstance(permissions, list) or any(permission not in self.__permissions for permission in permissions):
            return False
        
        # Assign new api key
        self.__sessions[key] = {'time_frame': {'start': time.time()}, 'permissions': permissions}
        
        return True
        
    def __init__(self):
        """
        Initialize permission list and session dict
        """

        self.__permissions: Dict[str, List[str]] = {'READ': ['GET', 'HEAD'], 'CREATE': ['POST'], 'UPDATE': ['PUT', 'PATCH'], 'DELETE': ['DELETE']} # Available permissions
        self.__sessions: Dict = {} # Api keys provided as -> key: {time_frame: {start: (time)}, permissions: [...]} 