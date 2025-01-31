import pytest
from typing import List, Dict, Tuple
from ExampleFlaskAPI.utils import Utils
    
def test_check_structure():
    """Test for checking correct structures"""

    structure: StructureDict = {'name': (str, True)}
    
    assert Utils.check_structure([{'name': 'test'}], structure) == True
    assert Utils.check_structure([{'name': 123}], structure) == False
    assert Utils.check_structure([{'name': 'test', 'parent_name': 'test'}], structure) == False
    assert Utils.check_structure([{}], structure) == False

def test_structure_process():
    """Test for checking correct value"""

    structure: Tuple[type | Dict | List[type], bool] = (str, True)

    assert Utils.structure_process({'name': 'test'}, 'name', structure) == (True, True)
    assert Utils.structure_process({'name': 123}, 'name', structure) == (False, True)
    assert Utils.structure_process({'name': 'test', 'parent_name': 'test'}, 'name', structure) == (True, True)
    assert Utils.structure_process({}, 'name', structure) == (False, False)              