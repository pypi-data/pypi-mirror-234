from typing import Any
import pickle, os, sys

_config_root_path = os.path.join(os.path.expanduser('~'),'.kisaconf') 

_EXT = 'kisaconf'

if (not os.path.isdir(_config_root_path)) and os.system(f'mkdir "{_config_root_path}"'):
    sys.exit('failed to create config root path')

def _initTable(table:str):
    fout = os.path.join(_config_root_path,f'{table}.{_EXT}')
    if not os.path.isfile(fout):
        pickle.dump({}, open(fout,'wb'))

    return fout

def _getTableAndKey(path:str) -> list[str,str]:
    '''
    path: tableName/keyName eg 'table1/key1'

    @returns [table,key]
    '''
    if ('/' not in path) or (' ' in path) or path.startswith('/') or path.endswith('/'):
        raise ValueError('invalid key path given')

    return path.split('/')

def getValue(path:str) -> Any|None:
    '''
    path: tableName/keyName eg 'table1/key1'
    '''

    table, key = _getTableAndKey(path)

    return pickle.load(open(_initTable(table),'rb')).get(key)
    
def setValue(path:str, value:Any) -> bool:
    '''
    path: tableName/keyName eg 'table1/key1'
    '''
    table, key = _getTableAndKey(path)

    tableFile = _initTable(table)
    with open(tableFile,'rb') as fin:
        data = pickle.load(fin)

    data[key] = value

    with open(tableFile, 'wb') as fout:
        try: pickle.dump(data,fout)
        except: return False
    
    return True
