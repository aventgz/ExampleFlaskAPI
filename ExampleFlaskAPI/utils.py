import traceback
from typing import List, Dict, Tuple

StructureDict = Dict[str, Tuple[type | Dict | List[type], bool]]

class Utils:
    """
    A class containing utility functions
    """   

    @staticmethod
    def check_structure(data: List[Dict], structure: StructureDict) -> bool:
        """
        Check structure of provided data

        Args:
            data (List[Dict]): List of rows to check
            structure (StructureDict): Required structure

        Returns:
            bool: Return match condition
        """

        try:
            row: Dict
            for row in data:           
                counter: int = 0 # Correct key counter              
                key: str; value_info: Tuple[type | Dict | List[type], bool]

                for key, value_info in structure.items():
                    check: Tuple[bool, bool] = Utils.structure_process(row, key, value_info)
                    if not check[0]:
                        return False                    
                    counter += check[1] # Increases when a key is detected
                
                if len(row.keys()) != counter:
                    return False                          
            return True
        except Exception as e:
            traceback.print_exc() 
            return False

    @staticmethod         
    def structure_process(row: Dict, key: str, value_info: Tuple[type | Dict | List[type], bool]) -> Tuple[bool, bool]:
        """
        Process single attribute in row

        Args:
            row (Dict): Row to check
            key (str): Name of attribute required
            value_info (Tuple[type | Dict | List[type], bool] | Dict): Required structure

        Returns:
            Tuple[bool, bool]: Return match conditions
        """

        # Obtain information about value type and requirement status
        value_type: type; is_required: bool
        value_type, is_required = value_info
                    
        # Check for key
        if key not in row:
            if not is_required:
                return True, False
            return False, False
          
        # Proceed value if dictionary        
        if isinstance(value_type, dict):
            if not Utils.check_structure([row[key]], value_type):
                return False, True 
        # Check if value type match        
        elif not isinstance(row[key], value_type):
            return False, True
            
        return True, True