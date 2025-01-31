import traceback
import pymongo
from pymongo.client_session import ClientSession
from flask_pymongo import PyMongo
from typing import List, Dict

class DatabaseBridge:  
    """
    A class for sending requests to mongodb as an interface
    """       

    def start_session(self) -> pymongo.client_session.ClientSession:
        """
        Start mongodb session

        Returns:
            pymongo.client_session.ClientSession: Return mongodb session
        """
        
        try:            
            return self.__client.cx.start_session()
        except Exception as e:
            traceback.print_exc() 
            return None          
    
    def find(self, collection: str, condition: Dict, skip: int = 0, limit: int = -1) -> List:
        """
        Find rows with the given condition

        Args:
            collection (str): Collection name
            condition (Dict): Condition for query
            skip (int, optional): Number of elements to skip. Defaults to 0.
            limit (int, optional): Max number of elements to obtain. Defaults to -1.

        Returns:
            List: Return rows.
        """

        try:
            if(limit < 0):
                return list(self.__client.db[collection].find(condition).skip(skip))
            return list(self.__client.db[collection].find(condition).skip(skip).limit(limit))     
        except Exception as e:
            traceback.print_exc() 
            return []                 
            
    def find_one(self, collection: str, condition: Dict) -> Dict:
        """
        Find row with the given condition

        Args:
            collection (str): Collection name
            condition (Dict): Condition for query

        Returns:
            Dict: Return row
        """

        try:
            return self.__client.db[collection].find_one(condition)
        except Exception as e:
            traceback.print_exc() 
            return []    
            
    def insert_one(self, collection: str, row: Dict) -> List:
        """
        Insert row

        Args:
            collection (str): Collection name
            row (Dict): Row to insert

        Returns:
            List: Return insertion status
        """

        try:
            return self.__client.db[collection].insert_one(row)
        except Exception as e:
            traceback.print_exc() 
            return []   

    def insert_many(self, collection: str, rows: List[Dict]) -> List:
        """
        Insert many rows

        Args:
            collection (str): Collection name
            rows (Dict): Rows to insert

        Returns:
            List: Return insertion status
        """

        try:
            return self.__client.db[collection].insert_many(rows)
        except Exception as e:
            traceback.print_exc() 
            return []   
            
    def delete_many(self, collection: str, condition: Dict) -> List:
        """
        Delete many rows with given condition

        Args:
            collection (str): Collection name
            condition (Dict): Condition for query

        Returns:
            List: Return delete status
        """

        try:
            return self.__client.db[collection].delete_many(condition)
        except Exception as e:
            traceback.print_exc() 
            return []    

    def update_one(self, collection: str, condition: Dict, operation: Dict) -> List:
        """
        Update row with given condition

        Args:
            collection (str): Collection name
            condition (Dict): Condition for query
            operation (Dict): Values to change in a row

        Returns:
            List: Return update status
        """

        try:
            return self.__client.db[collection].update_one(condition, operation)
        except Exception as e:
            traceback.print_exc() 
            return []            
            
    def update_many(self, collection: str, condition: Dict, operation: Dict) -> List:
        """
        Update rows with given condition

        Args:
            collection (str): Collection name
            condition (Dict): Condition for query
            operation (Dict): Values to change in a rows

        Returns:
            List: Return update status
        """

        try:
            return self.__client.db[collection].update_many(condition, operation)
        except Exception as e:
            traceback.print_exc() 
            return [] 

    def get_collection_names(self) -> List[str]:
        """
        Get list of collection names

        Returns:
            List[str]: Return list of collection names
        """

        try:
            return self.__client.db.list_collection_names()
        except Exception as e:
            traceback.print_exc() 
            return []                                
  
    def __init__(self, client: PyMongo):
        """
        Assign mongo interface

        Args:
            client (PyMongo): Client for mongodb
        """

        self.__client = client