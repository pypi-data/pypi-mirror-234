'''
this modules handle data structure validation to ensure that
data is passed in expected formats/structures
'''

from typing import Any

def validate(instance:Any, structure:Any, path:str='$') -> dict:
    '''
    validate payload/instance against a pre-defined structure
    
    returns {
        'status':bool,
        'log':STRING
    }
    '''
    
    result = {'status':False, 'log':''}

    # when the structure is a block type/class eg dict,list,tuple,etc
    if type(structure)==type(type):
        if instance!=structure and not isinstance(instance, structure):
            result['log'] = f'E01: types not similar:: {path}, expected {str(structure)[7:-1]} but got {str(type(instance))[7:-1]}'
            return result
        result['status'] = True
        return result

    if not isinstance(instance,type(structure)):
        result['log'] = f'E02: types not similar:: {path}, expected {str(type(structure))[7:-1]} but got {str(type(instance))[7:-1]}'
        return result

    if isinstance(structure,dict):
        _path = path
        for key in structure:
            path = f'{_path}->{key}'
            if key not in instance:
                result['log'] = f'E03: missing key:: {path}'
                return result
            res = validate(instance[key],structure[key], path=path)
            if not res['status']:
                return res
    elif isinstance(structure,(list,tuple)):
        _path = path
        for index,item in enumerate(structure):
            path = f'{_path}->[#{index}]'
            if len(instance)<=index:
                result['log'] = f'E04: missing item at index:: {path}, expects {str(type(item))[7:-1] if not isinstance(item,type) else str(item)[7:-1]}'
                return result
            res = validate(instance[index],item, path=path)
            if not res['status']:
                return res

    result['status'] = True
    return result
