from Crypto.Cipher import AES
import base64
from Crypto.Util.Padding import unpad
import pandas as pd
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad
from pandas.core.series import Series
from .utils import modulereload


def decrypt(x: str, key:str) -> str:
    """
     Parameters
    ----------

    x: Input String
    key: Key to decrypt data, contact DWH admin to get key
    """
    check = str(x)
    if check and check != "None":
        x_bytes = base64.b64decode(x)
        encryption = AES.new(base64.b64decode(key), AES.MODE_CBC, x_bytes[0:16])
        return unpad(encryption.decrypt(x_bytes[16:]),16).decode('utf-8')


def decrypt_column(self, key):
    """
     Parameters
    ----------

    df: pandas.DataFrame
    col: str column want to decrypt
    key: Key to decrypt data, contact DWH admin to get key
    
    Return:
    pandas.core.series.Series
    """
    return self.apply(decrypt, args=(key,))


def encrypt(data, key):
    check = str(data)
    data = str(data)
    if check and check != "None":
        data = data.encode('utf-8')
        key = base64.b64decode(key)
        iv = get_random_bytes(16)
        cipher = AES.new(key, AES.MODE_CBC, iv=iv)
        ciphertext = cipher.encrypt(pad(data, AES.block_size))
        return base64.b64encode(iv+ciphertext).decode('utf-8')
    else:
        return ''
    
    
def encrypt_column(self, key):
    """
     Parameters
    ----------

    df: pandas.DataFrame
    col: str column want to encrypt
    key: Key to encrypt data, contact DWH admin to get key
    
    Return:
    pandas.core.series.Series
    """
    return self.apply(encrypt, args=(key,))

Series.decrypt_column = decrypt_column
Series.encrypt_column = encrypt_column
modulereload(pd)


