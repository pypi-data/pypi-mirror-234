import os, sys
import sqlite3
from types import SimpleNamespace

if sqlite3.sqlite_version_info[1]<38:
    sys.exit(f'we need sqlite3 v3.38.0+ to run this program. current version::{sqlite3.sqlite_version}')

MAX_FETCH_ITEMS = 8*1024

__EXT__ = 'sqlite3'

# you want this to throw erros in user-defined functions
sqlite3.enable_callback_tracebacks(True)

TRIGGERS:dict = {
    # eg
    # 'userActiveStateChange':{
    #     'table': 'users',
    #     'when': 'after', # before | after | instead of
    #     'action': 'update', # insert | update | delete
    #     'condition':'''
    #         old.active != new.active
    #     ''',
    #     'code':'''
    #         insert into logs values(
    #             datetime('now', '+03:00'), 
    #             new.addedBy, 
    #             "users.active: change "||old.active||"->"||new.active,
    #             "{}"
    #         )
    #     '''
    # },

}

# *********************************************************************
def _checkContext(method):
    '''
    this decorator will be used to enforce the calling of Api class instances
    from `with` contexts. this will ensure resources are always released as they
    should
    '''
    def _(self, *args, **kwargs):
        if not self._in_with_statement:
            raise Exception(f'method `db.Api.{method.__name__}` called from outside `with` statement/context')
        return method(self,*args, **kwargs)
    return _

class Api:
    def __init__(self, path:str, tables:dict = {}, readonly=True, bindingFunctions:list=[]):

        '''
        bindingFunctions:  Custom functions defined in python to be used by sqlite3. 
                           Each entry is in form (name:str, nargs:int, func:function)
        
        tables: dict[str,str]
                eg
                {
                    'credentials':"""
                        key             varchar(256) not null,
                        value           varchar(256) not null
                    """,
                    'users':"""
                        firstName       varchar(256) not null,
                        lastName        varchar(256) not null,
                        username        varchar(256) not null
                    """,
                }

        '''

        self._in_with_statement = False
        self.isOpen = False
        self.functions:dict = {}

        while path.endswith('/'): path = path[:-1]
        if not path.endswith(f'.{__EXT__}'):
            path += f'.{__EXT__}'

        path_root = os.path.split(path)[0]
        
        if (not os.path.isdir(path_root)) and os.system(f'mkdir -p "{path_root}"'):
            return

        if not os.path.isfile(path):
            initTables = True

        self.db:sqlite3.Connection = sqlite3.connect(path)
        self.cursor:sqlite3.Cursor = self.db.cursor();

        initTables = True if tables else False
        if initTables:
            for table in tables:
                self.cursor.execute(f'create table if not exists {table} ({tables[table]})')
            self.db.commit()
        
        self._bind_functions(bindingFunctions)
        
        self.isOpen = True

        if readonly:
            self.cursor.execute(f'''
            pragma query_only = ON;   -- disable changes
            ''')

    def _bind_functions(self, functions):
        for entry in functions:
            if entry[0] in self.functions: continue
            self.db.create_function(*entry)
            self.functions[entry[0]] = entry[-1]

    @_checkContext
    def execute(self, cmd:str, cmdData:list=[], commit:bool=False):
        try:
            self.cursor.execute(cmd,cmdData)
            if commit: self.db.commit() # ?
            return True
        except:
            return False

    @_checkContext
    def fetch(self, table:str, columns:list, condition:str, conditionData:list, limit:int=MAX_FETCH_ITEMS, returnDicts:bool=False, returnNamespaces:bool=False) -> list:
        '''
        fetch databse data given condition and conditionValues eg
        
        apiObj.fetch(
            'users',
            ['username','clearance'],
            'active=? and username=? and password=?',
            [1,'test','123']
        )
        '''
        assert (limit>0 and limit<=MAX_FETCH_ITEMS), f'please set a limit on the returned rows. maximum should be {MAX_FETCH_ITEMS}'

        condition = condition.strip() or '1'
        assert(len(condition.strip()))
        
        if columns in [['*']]:
            self.cursor.execute(f'select * from {table} where {condition} limit {limit}',conditionData)
            columns = [description[0] for description in self.cursor.description]

        self.cursor.execute(f"select {','.join(columns)} from {table} where {condition} limit {limit}",conditionData)
        
        if not (returnDicts or returnNamespaces):
            return self.cursor.fetchall()

        cols = [_[0] for _ in self.cursor.description]

        if returnDicts:
            return [dict(zip(cols,_)) for _ in self.cursor.fetchall()]

        # namepsaces...
        if [_ for _ in cols if (
            (' ' in _) or not (
                'a'<=_[0]<='z' or \
                'A'<=_[0]<='Z' or \
                '_'==_[0]
            )
        )]:
            raise TypeError('one or more column names is invalid as a key for namespaces')

        return [SimpleNamespace(**dict(zip(cols,_))) for _ in self.cursor.fetchall()]

    @_checkContext
    def insert(self, table:str, data:list) -> bool:
        self.cursor.execute(f'select * from {table}')
        column_value_placeholders = ['?' for description in self.cursor.description]
        
        try:
            if isinstance(data[0],list) or isinstance(data[0],tuple):
                self.cursor.executemany(f'insert into {table} values ({",".join(column_value_placeholders)})',data)
            else:
                self.cursor.execute(f'insert into {table} values ({",".join(column_value_placeholders)})',data)
            self.db.commit()
            return True
        except:
            return False

    @_checkContext
    def update(self, table:str, columns:list, columnData:list, condition:str, conditionData:list):

        if columns in [['*']]:
            self.cursor.execute(f'select * from {table}')
            columns = [description[0] for description in self.cursor.description]

        try:
            self.cursor.execute(f'update {table} set {"=?,".join(columns)}=? where {condition}',columnData+conditionData)
            self.db.commit()
            return True
        except:
            return False

    @_checkContext
    def delete(self, table:str, condition:list, conditionData:list):
        try:
            self.cursor.execute(f'delete from {table} where {condition}',conditionData)
            self.db.commit()
            return True
        except:
            return False

    @_checkContext
    def close(self):
        if self.isOpen:
            self.db.execute('pragma optimize;')
            self.db.commit()
            self.db.close()
            # self.db, self.cursor = None,None
            self.isOpen = False

    @_checkContext
    def release(self):
        return self.close()

    # methods to add context to the handle
    def __enter__(self) -> 'Api':
        self._in_with_statement = True
        return self

    def __exit__(self, *args) -> bool:
        # args = [exc_type, exc_value, traceback]
        self.release()
        self._in_with_statement = False

        # False=propagate exceptions, True=supress them
        # you want to propagate exceptions so that the calling code can know what went wrong
        if args[0] is None:
            return True
        else:
            return False

if __name__=='__main__':
    pass