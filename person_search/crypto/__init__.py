# -*- mode: python; coding: utf-8 -*-
"""
"""
# INPROD:
#
#  tl;dr -- Crypto is hard, and this would require some research to do properly.
#
# This code does what it says, but I'm under no illusion that this is safe to use in production. I choose the path of least Resistance here and use symmetric encryption using the popular `cryptography` module. Depending on the use case, it might be better to focus on making sure no one ever gets to the data in the first place. One possible case where we'd want to use asymmetric encryption is where we have a multi-master cluster of database servers, in which case we could have only the public key on these hosts to permit writting. Reading is a different problem. If read performance is not critical, just have one host with the private key?
# After implementing this I find ``Fernet seems not to be maintained anymore. There has been no updates for the spec in three years. Original developers are in radio silence`` [https://appelsiini.net/2017/branca-alternative-to-jwt/]

# this code is based upon example code in the docs: https://cryptography.io/en/latest/fernet/#using-passwords-with-fernet

import os
import base64
from cryptography.fernet import InvalidToken
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# INPROD: The secret should be on disk maybe? or in memory only, somehow.
# There's not much point in using asymmetric encryption here.
SECRET = None
KEY = None

def get_secret():
    """Use the contents of `~/.ps_secret` if it exsists. Otherwise just use the string `secret`
    """
    global SECRET
    if SECRET is not None:
        return SECRET
    secret_path = os.path.expanduser('~/.ps_secret')
    if os.path.exists(secret_path):
        with open(secret_path, 'rb') as f:
            SECRET = f.read()
    else:
        SECRET = b'secret'
    return SECRET

def get_key():
    """Get the "key" for symmetric Fernet encryption. If we've already calculated it, return that.
    """
    global KEY
    if KEY is not None:
        return KEY

    salt_path = os.path.expanduser('~/.ps_salt')
    if not os.path.exists(salt_path):
        salt = os.urandom(16)
        with open(salt_path, 'wb') as f:
            f.write(salt)
    else:
        with open(salt_path, 'rb') as f:
            salt = f.read()
    
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    KEY = base64.urlsafe_b64encode(kdf.derive(get_secret()))
    return KEY

def crypt13(message, decrypt=False):
    """ROT13 cipher for testing
    """
    import codecs
    return codecs.getencoder('rot-13')(message)[0]
    
def crypt(message, decrypt=False):
    """Perform simple symmetric encryption of `message`. `decrypt=True` to decrypt
    """
    f = Fernet(get_key())
    if decrypt:
        try:
            return f.decrypt(message)
        except InvalidToken as e:
            raise Exception('Wrong secret. Did you lose `~/.ps_secret` or `~/.ps_salt`? [%s]' % repr(e))
    else:
        return f.encrypt(message)

if __name__ == '__main__':

    # how I did very basic testing:
    import sys
    if len(sys.argv) == 1: # no args: encrypt
        sys.exit()
        x = crypt('my secret')
        open('/tmp/fasd', 'wb').write(x)
    else:  # otherwise decrypt
        # mess around with the ~/.ps_* files here...
        x = open('/tmp/fasd', 'rb').read()
        print crypt(x, decrypt=True)
