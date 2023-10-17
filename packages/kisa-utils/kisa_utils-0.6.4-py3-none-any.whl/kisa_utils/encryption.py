import subprocess
import hashlib

__ECRYPTION_SALT:str = 'kisa.encrypt@2023'
__HASH_SALT:str = 'k.i.s.a.hash@+9JI0'

def __encrypt(msg:str, returnBytes:bool=False, pswd:str=__ECRYPTION_SALT) -> str|bytes:
    '''
    this encryption is by no means meant to be secure. its simple obfusication really
    '''
    try:
        out = subprocess.run(f'''echo '{msg}' | openssl aes-256-cbc -a -iter=10 -pass pass:{pswd}''',check=True,shell=True,capture_output=True, text=True).stdout.strip()
        return out.encode('utf-8') if returnBytes else out
    except:
        raise ValueError('error calling <openssl> is it installed?')

def __decrypt(encryptedMsg:str, returnBytes:bool=False, pswd:str=__ECRYPTION_SALT) -> str|bytes:
    try:
        out=subprocess.run(f'''echo '{encryptedMsg}' | openssl aes-256-cbc -d -a -iter=10 -pass pass:{pswd}''',check=True,shell=True,capture_output=True, text=True).stdout.strip()
        return out.encode('utf-8') if returnBytes else out
    except:
        raise ValueError('error calling <openssl> is it installed?')

def __hash(msg:str|bytes, returnBytes:bool=False, salt:str|bytes = __HASH_SALT) -> str|bytes:
    if isinstance(msg,str):
        msg = bytes(msg,'utf-8')
    if isinstance(salt,str):
        salt = bytes(salt,'utf-8')
    
    # `sha3_256` is prefered to `sha256`
    _hash = hashlib.sha3_256(msg+salt).hexdigest()
    return bytes(_hash,'utf-8') if returnBytes else _hash

def decrypt(encryptedMsg:str, returnBytes:bool=False) -> str|bytes:
    return __decrypt(encryptedMsg, returnBytes=returnBytes)

def encrypt(msg:str, returnBytes:bool=False) -> str|bytes:
    return __encrypt(msg, returnBytes=returnBytes)

def hash(msg:str|bytes, returnBytes:bool=False) -> str|bytes:
    return __hash(msg, returnBytes=returnBytes)
