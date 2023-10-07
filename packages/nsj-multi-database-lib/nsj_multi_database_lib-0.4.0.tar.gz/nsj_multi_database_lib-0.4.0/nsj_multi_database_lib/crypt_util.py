from cryptography.fernet import Fernet

from nsj_multi_database_lib.settings import get_crypt_key

def decrypt(value: str):
    fernet = Fernet(get_crypt_key())

    # Decypt user
    value = value.encode()
    value = fernet.decrypt(value).decode()

    return value
