from cryptography.fernet import Fernet

@staticmethod
def createKey():
    """
        Generate key and return it.
    """
    return Fernet.generate_key()

@staticmethod
def encryptData(key, data):
    """
        Encrypts data
    """
    return Fernet(key).encrypt(data.encode())

@staticmethod
def decryptData(key, data):
    """
        Decrypts data
    """
    return (Fernet(key).decrypt(data)).decode()