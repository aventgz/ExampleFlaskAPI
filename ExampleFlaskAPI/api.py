import traceback
from ExampleFlaskAPI.authorization import Authorization
from ExampleFlaskAPI.database_bridge import DatabaseBridge
from ExampleFlaskAPI.endpoint_item import EndpointItem
from ExampleFlaskAPI.endpoint_category import EndpointCategory
from ExampleFlaskAPI.endpoint_search_items import EndpointSearchItems

class API:
    """
    A class for configuring the API
    """   

    def __setup_authorization(self, authorization: Authorization):
        """
        Initialize authorization and setup example keys with permissions

        Args:
            authorization (Authorization): Authorization for API   
        """

        self.__authorization: Authorization = authorization         

    def __setup_endpoints(self):
        """
        Create endpoints and routes
        """

        api_prefix: str = '/api/v1'
        
        self.__endpoints: Dict[str, Endpoint] = {}
            
        self.__endpoints['item'] = EndpointItem(self.__mongo, self.__codes, self.__authorization)
        self.__endpoints['category'] = EndpointCategory(self.__mongo, self.__codes, self.__authorization)
        self.__endpoints['search_items'] = EndpointSearchItems(self.__mongo, self.__codes, self.__authorization)

        # Assign endpoints    
        self.__app.route(api_prefix + '/item/<serial_number>', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])(self.__endpoints['item'].route_item)
        self.__app.route(api_prefix + '/item', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])(self.__endpoints['item'].route_item)
                      
        self.__app.route(api_prefix + '/category/<name>', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])(self.__endpoints['category'].route_category)
        self.__app.route(api_prefix + '/category', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])(self.__endpoints['category'].route_category)
            
        self.__app.route(api_prefix + '/search/items', methods=['GET'])(self.__endpoints['search_items'].route_search_items)

    def __init__(self, app: any, mongo: DatabaseBridge, authorization: Authorization):
        """
        Assign flask app and database bridge, provide custom status codes with messages

        Args:
            app (any): Flask app       
            mongo (DatabaseBridge): Bridge to work on mongodb    
            authorization (Authorization): Authorization for API    
        """

        self.__app: any = app
        
        self.__mongo: DatabaseBridge = mongo
        
        self.__codes: Dict[int, Dict[str, str]] = {                     
            1200: {
                'en-EN': 'Request done.',
                'pl-PL': 'Żądanie wykonane.'
            },
            1401: {
                'en-EN': 'Serial number(s) must be provided.',
                'pl-PL': 'Należy podać numer(y) seryjny/e.'
            },
            1402: {
                'en-EN': 'No item has been removed.',
                'pl-PL': 'Żaden przedmiot nie został usunięty.'
            },
            1403: {
                'en-EN': 'The input data must be provided in the form of a list.',
                'pl-PL': 'Dane wejściowe należy podać w formie listy.'
            },
            1404: {
                'en-EN': 'Category name(s) must be provided.',
                'pl-PL': 'Należy podać nazwy kategorii.'
            },
            1405: {
                'en-EN': 'No categories have been removed.',
                'pl-PL': 'Żadne kategorie nie zostały usunięte.'
            },
            1406: {
                'en-EN': 'Wrong search type provided.',
                'pl-PL': 'Błędny typ wyszukiwania.'
            }        
        }
        
        self.__setup_authorization(authorization)
        
        self.__setup_endpoints()