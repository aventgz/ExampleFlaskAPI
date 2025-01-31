import werkzeug
import traceback
from typing import Callable, Dict, Union, List, Tuple
from ExampleFlaskAPI.endpoint import Endpoint, OperationStatusDict

class EndpointItem(Endpoint):  
    """
    A child class to handle item-related requests
    """   

    def route_item(self, **kwargs) -> str:
        """
        Forwarding to the main routing function

        Args:
            **kwargs: arguments passed by Flask

        Returns:
            str: Return server response
        """

        return self._route(**kwargs)
        
    def _GET(self, request: werkzeug.local.LocalProxy, serial_number: str = None) -> Tuple[int, bool, int, List]:
        """
        Implementation of GET method for getting items

        Args:
            request (werkzeug.local.LocalProxy): Flask request
            serial_number (str): Serial number of item

        Returns:
            Tuple[int, bool, int, List]: Return response
        """

        # Get serial numbers
        item_serials: str | List[str] = request.args.get('serial_number', type=str)

        if item_serials:
            item_serials: List[str] = [str(serial) for serial in item_serials.split(',')]
  
        if not item_serials:
            if serial_number:
                item_serials = [serial_number]
            else:
                return 400, False, 1401       
        
        return 200, True, 1200, self._mongo.find('Item', {'serial_number': {'$in': item_serials}})

    @Endpoint.required_structure({
        'serial_number': (str, True),
        'name': (str, True),
        'description': (str, True),
        'category': (str, True),
        'price': (float, True),
        'location': (
            {
                'room': (int, True),
                'bookcase': (int, True),
                'shelf': (int, True),
                'cuvette': (int, True),
                'column': (int, True),
                'row': (int, True)
            },
            True
        )      
    })        
    def _POST(self, request: werkzeug.local.LocalProxy) -> Tuple[int, bool, int, List]:
        """
        Implementation of POST method for adding items

        Args:
            request (werkzeug.local.LocalProxy): Flask request

        Returns:
            Tuple[int, bool, int, List]: Return response
        """

        # Get items
        items: List = request.get_json()        
        
        serials: List[str] = []
               
        statuses: List[OperationStatusDict] = []
      
        for item in items:
            serial: str; status: OperationStatusDict

            serial, status = self.__post_process(item, serials)
            
            serials.append(serial)
            statuses.append(status)
            
        return 200, True, 1200, statuses

    @Endpoint.required_structure({
        'serial_number': (str, True),
        'change': (
            {
                'name': (str, True),
                'description': (str, True),
                'category': (str, True),
                'price': (float, True),
                'location': (
                    {
                        'room': (int, True),
                        'bookcase': (int, True),
                        'shelf': (int, True),
                        'cuvette': (int, True),
                        'column': (int, True),
                        'row': (int, True)
                    },
                    True
                )
            },
            True
        )
    })
    def _PUT(self, request: werkzeug.local.LocalProxy) -> Tuple[int, bool, int, List]:
        """
        Implementation of PUT method for editing items

        Args:
            request (werkzeug.local.LocalProxy): Flask request

        Returns:
            Tuple[int, bool, int, List]: Return response
        """

        return self.__update(request)
        
    @Endpoint.required_structure({
        'serial_number': (str, True),
        'change': (
            {
                'name': (str, False),
                'description': (str, False),
                'category': (str, False),
                'price': (float, False),
                'location': (
                    {
                        'room': (int, False),
                        'bookcase': (int, False),
                        'shelf': (int, False),
                        'cuvette': (int, False),
                        'column': (int, False),
                        'row': (int, False)
                    },
                    False
                )      
            },
            True
        )
    })
    def _PATCH(self, request: werkzeug.local.LocalProxy) -> Tuple[int, bool, int, List]:
        """
        Implementation of PATCH method for editing items

        Args:
            request (werkzeug.local.LocalProxy): Flask request

        Returns:
            Tuple[int, bool, int, List]: Return response
        """

        return self.__update(request)
     
    def _DELETE(self, request: werkzeug.local.LocalProxy, serial_number: str) -> Tuple[int, bool, int, List]:
        """
        Implementation of DELETE method for deleting items

        Args:
            request (werkzeug.local.LocalProxy): Flask request
            serial_number (str): Serial number of item

        Returns:
            Tuple[int, bool, int, List]: Return response
        """

        # Get serial numbers
        items_serials: str | List[str] = request.args.get('serial_number', type=str)
        
        if items_serials:
            items_serials = [str(serial) for serial in items_serials.split(',')]
            
        if not items_serials:
            if not serial_number:
                return 400, False, 1401                
            items_serials = [serial_number]        
        
        serials: List[str] = []
        
        statuses: List[OperationStatusDict] = []     
        
        for item in items_serials:
            serial: str; status: OperationStatusDict            
            serial, status = self.__delete_process(item, serials)

            serials.append(serial)
            statuses.append(status)
                    
        return 200, True, 1200, statuses   

    def __post_process(self, item: Dict, serials: List[str]) -> Tuple[str, OperationStatusDict]:
        """
        Process add of each item

        Args:
            item (Dict): item informations
            serials (List[str]): List of serials already added in current POST operation

        Returns:
            Tuple[str, OperationStatusDict]: Return serial number and status of operation
        """

        serial_number_response: str = ''
        
        # Assign serial number
        if 'serial_number' in item:
            serial_number_response: str = str(item['serial_number'])                   
        
        # Start mongo transaction
        with self._mongo.start_session() as session:
            with session.start_transaction():
                # Check if serial number exists
                if self._mongo.find_one('Item', {'serial_number': item['serial_number']}) or item['serial_number'] in serials:
                    return serial_number_response, {'id': serial_number_response, 'status': False, 'message': 'Serial number already exist.'}
                
                # Get category
                if len(item['category']) > 0:
                    category: OperationStatusDict = self.__check_category(serial_number_response, item['category'])
                    if (category):
                        return category

                # Validate price
                if item['price'] < 0:
                    return serial_number_response, {'id': serial_number_response, 'status': False, 'message': 'Price must be greater than 0.'}            
                        
                self._mongo.insert_one('Item', item)
                    
        return serial_number_response, {'id': serial_number_response, 'status': True, 'message': 'Item added to database.'}       

    def __delete_process(self, item: str, serials: List[str]) -> Tuple[str, OperationStatusDict]:
        """
        Process delete of each item

        Args:
            item (str): Serial number
            serials (List[str]): List of serials already deleted in current DELETE operation

        Returns:
            Tuple[str, OperationStatusDict]: Return serial number and status of operation
        """

        serial_number_response: str = item              
        
        # Start mongo transaction
        with self._mongo.start_session() as session:
            with session.start_transaction():
                # Check if serial number exists
                if item in serials:
                    return serial_number_response, {'id': serial_number_response, 'status': False, 'message': 'Serial number already deleted.'}

                if self._mongo.delete_many('Item', {'serial_number': {'$in': [item]}}).deleted_count > 0:
                    return serial_number_response, {'id': serial_number_response, 'status': True, 'message': 'Item deleted from database.'} 

        return serial_number_response, {'id': serial_number_response, 'status': False, 'message': 'Delete action failed.'}            

    def __update(self, request: werkzeug.local.LocalProxy) -> Tuple[int, bool, int, List]:
        """
        Update function for PATCH and PUT

        Args:
            request (werkzeug.local.LocalProxy): Flask request

        Returns:
            Tuple[int, bool, int, List]: Return response
        """

        # Get items
        items: List = request.get_json()
        
        if not isinstance(items, list):
            return 400, False, 1403
        
        statuses: List[OperationStatusDict] = []     
        
        for item in items:            
            statuses.append(self.__update_process(item))
                    
        return 200, True, 1200, statuses   

    def __update_process(self, item: Dict) -> OperationStatusDict:
        """
        Process update of each item

        Args:
            item (Dict): Item informations

        Returns:
            OperationStatusDict: Return status of operation
        """

        serial_number_response: str = item['serial_number']
        
        update: Dict = item['change']
        
        # Begin mongodb transaction
        with self._mongo.start_session() as session:
            with session.start_transaction():
                # Get category
                if len(update['category']) > 0:
                    category: OperationStatusDict = self.__check_category(serial_number_response, update['category'])
                    if (category):
                        return category

                # Validate price
                if 'price' in update and update['price'] < 0:
                    return serial_number_response, {'id': serial_number_response, 'status': False, 'message': 'Price must be greater than 0.'}                   

                if self._mongo.update_one('Item', {'serial_number': item['serial_number']}, {'$set': update}).modified_count > 0:
                    return {'id': serial_number_response, 'status': True, 'message': 'Item updated.'}  
                    
        return {'id': serial_number_response, 'status': False, 'message': 'No modifications were made.'}

    def __check_category(self, serial_number: str, category_name: str) -> OperationStatusDict:
        """
        Check if category exist and if have parent

        Args:
            serial_number (str): Serial number of item
            category_name (str): Category of item

        Returns:
            OperationStatusDict: Return status of operation
        """        

        category: Dict = self._mongo.find_one('Category', {'name': category_name})
                    
        if not category:
            return {'id': serial_number, 'status': False, 'message': 'Category does not exist.'}

        if self._mongo.find_one('Category', {'parent_name': category_name}):    
            return {'id': serial_number, 'status': False, 'message': 'Choose other category than parent.'}      

        return None
