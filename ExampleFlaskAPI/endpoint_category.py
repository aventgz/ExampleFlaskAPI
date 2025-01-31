import werkzeug
import traceback
from typing import List, Dict, Tuple
from ExampleFlaskAPI.endpoint import Endpoint, OperationStatusDict

class EndpointCategory(Endpoint): 
    """
    A child class to handle category-related requests
    """   

    def route_category(self, **kwargs) -> str:
        """
        Forwarding to the main routing function

        Args:
            **kwargs: arguments passed by Flask

        Returns:
            str: Return server response
        """

        return self._route(**kwargs)
     
    def _GET(self, request: werkzeug.local.LocalProxy, name: str = None) -> Tuple[int, bool, int, List]:
        """
        Implementation of GET method for getting categories

        Args:
            request (werkzeug.local.LocalProxy): Flask request
            name (str): Name of category

        Returns:
            Tuple[int, bool, int, List]: Return response
        """

        # Get category names
        category_names: str | List[str]= request.args.get('name', type=str)

        if category_names:
            category_names = [str(name) for name in category_names.split(',')]

        if not category_names:
            if name:
                category_names = [name]
            else:
                return 400, False, 1404             

        return 200, True, 1200, self._mongo.find('Category', {'name': {'$in': category_names}})
        
    @Endpoint.required_structure({
        'name': (str, True),             
        'parent_name': (str, True)            
    })        
    def _POST(self, request: werkzeug.local.LocalProxy) -> Tuple[int, bool, int, List]:
        """
        Implementation of POST method for adding categories

        Args:
            request (werkzeug.local.LocalProxy): Flask request

        Returns:
            Tuple[int, bool, int, List]: Return response
        """

        # Get categories
        categories: List = request.get_json()
        
        names: List[str] = []
               
        statuses: List[OperationStatusDict] = []
        
        for category in categories:
            name: str; status: OperationStatusDict
            name, status = self.__post_process(category, names)
            
            names.append(name)
            statuses.append(status)
            
        return 200, True, 1200, statuses 
    
    @Endpoint.required_structure({
        'name': (str, True),
        'change': (
            {
                'parent_name': (str, True)
            },
            True
        )
    })
    def _PUT(self, request: werkzeug.local.LocalProxy) -> Tuple[int, bool, int, List]:
        """
        Implementation of PUT method for editing categories

        Args:
            request (werkzeug.local.LocalProxy): Flask request

        Returns:
            Tuple[int, bool, int, List]: Return response
        """

        return self.__update(request)
        
    @Endpoint.required_structure({
        'name': (str, True),
        'change': (
            {
                'parent_name': (str, False)
            },
            False
        )
    })
    def _PATCH(self, request: werkzeug.local.LocalProxy) -> Tuple[int, bool, int, List]:
        """
        Implementation of PATCH method for editing categories

        Args:
            request (werkzeug.local.LocalProxy): Flask request

        Returns:
            Tuple[int, bool, int, List]: Return response
        """

        return self.__update(request)
     
    def _DELETE(self, request: werkzeug.local.LocalProxy, name: str = None) -> Tuple[int, bool, int, List]:
        """
        Implementation of DELETE method for deleting categories

        Args:
            request (werkzeug.local.LocalProxy): Flask request
            name (str): Name of category

        Returns:
            Tuple[int, bool, int, List]: Return response
        """

        # Get categories names
        categories_names: str | List[str] = request.args.get('name', type=str)
        
        if categories_names:
            categories_names = [str(name) for name in categories_names.split(',')]
            
        if not categories_names: 
            if name:
                categories_names = [name]
            else:
                return 400, False, 1404
        
        statuses: OperationStatusDict = []
        
        for category_name in categories_names:
            statuses.append(self.__delete_process(category_name))
            
        return 200, True, 1200, statuses        

    def __post_process(self, category: Dict, names: List[str]) -> Tuple[str, OperationStatusDict]:
        """
        Process each category addition

        Args:
            category (Dict): Category informations
            names (List[str]): List of names already added in current POST operation

        Returns:
            Tuple[str, OperationStatusDict]: Return name and status of operation
        """

        # Retrieve category name
        name_response: str = self.__category_name(category)
                
        if len(name_response) < 1:
            return '', {'id': '', 'status': False, 'message': 'Need to provide name.'}
         
        # Begin mongodb transaction
        with self._mongo.start_session() as session:
            with session.start_transaction(): 
                # Check if category exist
                if self._mongo.find_one('Category', {'name': name_response}) or name_response in names:
                    return name_response, {'id': name_response, 'status': False, 'message': 'Name already exist.'}
                    
                # Check for parent category    
                if len(category['parent_name']) > 0 and self._mongo.find_one('Item', {'category': category['parent_name']}):
                    category['name'], {'id': name_response, 'status': True, 'message': 'Parent category cannot have assigned items.'}  
                        
                self._mongo.insert_one('Category', category)
                                                          
        return category['name'], {'id': name_response, 'status': True, 'message': 'Category added to database.'}      

    def __delete_process(self, category_name: str) -> OperationStatusDict:
        """
        Process deletion of each category

        Args:
            category_name (str): Name of category

        Returns:
            OperationStatusDict: Return status of operation
        """

        name_response = category_name            
        
        # Begin mongodb transaction
        with self._mongo.start_session() as session:
            with session.start_transaction():
                # Get category
                category: Dict = self._mongo.find_one('Category', {'name': category_name}) #checktype
                    
                if not category:
                    return {'id': category_name, 'status': False, 'message': 'Name does not exist.'}

                categories_to_check: List[str] = self.__categories_to_check(category_name)
                
                # Check if have items                      
                if self._mongo.find_one('Item', {'category': category_name}):
                    return {'id': category_name, 'status': False, 'message': 'Category cannot be deleted, because have items assigned.'}

                # Remove parents              
                if len(categories_to_check) > 0 and self._mongo.update_many('Category', {'name': {'$in': categories_to_check}}, {'$set': {'parent_name': ''}}).modified_count <= 0:
                    return {'id': category_name, 'status': False, 'message': 'Category cannot be deleted.'}
                 
                # Delete category
                if self._mongo.delete_many('Category', {'name': category_name}).deleted_count > 0:
                    return {'id': category_name, 'status': True, 'message': 'Category deleted.'}

        return {'id': category_name, 'status': False, 'message': 'Category not deleted.'}        

    def __categories_to_check(self, category_name: str) -> List[str]:
        """
        Get the categories to check further

        Args:
            category_name (str): Name of category

        Returns:
            List[str]: Return list of categories
        """
                      
        categories_to_check: List = self._mongo.find('Category', {'parent_name': category_name})
                        
        if not categories_to_check:
            return []

        return categories_to_check                     

    def __update(self, request: werkzeug.local.LocalProxy) -> Tuple[int, bool, int, List]:
        """
        Update function for PATCH and PUT

        Args:
            request (werkzeug.local.LocalProxy): Flask request

        Returns:
            Tuple[int, bool, int, List]: Return response
        """

        # Get categories
        categories: List = request.get_json()        
               
        statuses: List[OperationStatusDict] = []

        for category in categories:
            statuses.append(self.__update_process(category))
            
        return 200, True, 1200, statuses

    def __update_process(self, category: Dict) -> OperationStatusDict:
        """
        Process each category update

        Args:
            category (Dict): Category informations

        Returns:
            OperationStatusDict: Return status of operation
        """

        name_response: str = self.__category_name(category)
                
        if len(name_response) < 1:
            return {'id': name_response, 'status': False, 'message': 'Missing name.'}
        
        # Begin mongodb transaction
        with self._mongo.start_session() as session:
            with session.start_transaction(): 
                # Check if category exist
                if not self._mongo.find_one('Category', {'name': name_response}):
                    return {'id': name_response, 'status': False, 'message': 'Name not exists.'}
                    
                update: Dict = category['change']
                  
                if 'parent_name' in update and len(update['parent_name']) > 0:
                    if name_response == update['parent_name']:
                        return {'id': name_response, 'status': False, 'message': 'Cannot set same category as parent.'}

                    # Check if already exist
                    if not self._mongo.find_one('Category', {'name': update['parent_name']}):
                        return {'id': name_response, 'status': False, 'message': 'Parent category not exists.'}

                    # Check if parent have items assigned
                    if self._mongo.find_one('Item', {'category': update['parent_name']}):                  
                        return {'id': name_response, 'status': False, 'message': 'Category cannot be parent.'} 
                                                      
                # Update category               
                if self._mongo.update_one('Category', {'name': name_response}, {'$set': update}).modified_count > 0:
                    return {'id': name_response, 'status': True, 'message': 'Category changed.'}
                
                return {'id': name_response, 'status': False, 'message': 'No modifications were made.'}    
        
    def __category_name(self, category: Dict) -> str:
        """
        Get category name

        Args:
            category (Dict): Category informations

        Returns:
            str: Return category name if found
        """

        # Retrieve category name
        if 'name' in category:
            return str(category['name'])

        return ''
        
    def __category_check_parent(self, condition: Dict, name: str, base: bool) -> OperationStatusDict:
        """
        Check for category parent

        Args:
            condition (Dict): Condition to find category
            name (str): Category name
            base (bool): Check if category is base

        Returns:
            OperationStatusDict: Return status of operation
        """

        # Check for parent category
        parent_category: Dict = self._mongo.find_one('Category', condition)
          
        if not parent_category:
            return {'id': name, 'status': False, 'message': 'Parent category does not exist.'}
                            
        if base and parent_category.get('parent_name'):
            return {'id': name, 'status': False, 'message': 'Choose base category as parent.'}
            
        return None
