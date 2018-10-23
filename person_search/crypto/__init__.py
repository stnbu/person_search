# -*- mode: python; coding: utf-8 -*-
"""Simple cryptography helper functions

    crypt('clear_string') --> 'encrypted_string'
    crypt('encrypted_string', decrypt=True) --> 'clear_string'
"""
# INPROD:
#
#  tl;dr -- Crypto is hard, and this would require some research to do properly.
#
# This code does what it says, but I'm under no illusion that this is safe to
# use in production. I chose the path of least resistance here and use symmetric
# encryption using the ``cryptography`` package. Depending on the use case,
# it might be better to focus on making sure no one ever gets to the data in the
# first place. One possible case where we'd want to use asymmetric encryption is
# where we have a multi-master cluster of database servers, in which case we
# could have only the public key on these hosts to permit writing. Reading is a
# different problem. If read performance is not critical, just have one host
# with the private key?
#
# After implementing I find this: ``Fernet seems not to be maintained
# anymore. There has been no updates for the spec in three years. Original
# developers are in radio silence``
# [https://appelsiini.net/2017/branca-alternative-to-jwt/]

# this code is based upon example code in the docs:
# https://cryptography.io/en/latest/fernet/#using-passwords-with-fernet

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

import os
import codecs
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


def log_io(crypt_func):
    """Log i/o of crypto functions: Input (message) and output (return value)
    are logged in human-readable
    """
    def wrapper(message, decrypt=False):
        mode = ['encrypting', 'decrypting'][decrypt]
        log_output = '`%s()`: %s: we got %s as input, ' % (
            crypt_func.__name__,
            mode,
            message
        )
        result = crypt_func(message, decrypt)
        log_output += 'we are returning the value %s' % result
        logger.debug(log_output)
        return result
    return wrapper


def get_secret():
    """Use the contents of `~/.ps_secret` if it exists. Otherwise just use the
    string `secret`
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
    """Get the "key" for symmetric Fernet encryption. If we've already
    calculated it, return that.
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


@log_io
def crypt13(message, decrypt=False):
    """ROT13 cipher for testing
    """
    def rot13(message):
        """We put an `E:` in front of the "encrypted" version. This helper
        function does just ROT13
        """
        return codecs.getencoder('rot-13')(message)[0]

    if decrypt:
        return rot13(message[2:])
    else:
        return 'E:' + rot13(message)


@log_io
def crypt(message, decrypt=False):
    """Perform simple symmetric encryption of `message`. `decrypt=True` to
    decrypt

    Input can be bytes (utf-8) or a string, which is immediately converted to
    bytes. Return value is always bytes (utf-8)
    """

    if not isinstance(message, bytes):
        message = message.encode('utf-8')

    f = Fernet(get_key())
    if decrypt:
        try:
            result = f.decrypt(message)
        except InvalidToken as e:
            raise Exception(
                'Wrong secret. Did you lose `~/.ps_secret` or `~/.ps_salt`? '
                '[%s]' % repr(e))
    else:
        result = f.encrypt(message)

    return result.decode('utf-8')


if __name__ == '__main__':

    assert crypt13('foo') == 'E:sbb', 'crypt13 appears to be broken.'
    assert crypt13(
            'E:sbb', decrypt=True) == 'foo', 'crypt13 appears to be broken.'

    # how I did very basic testing:
    import sys
    if len(sys.argv) == 1:  # no args: encrypt
        sys.exit()
        x = crypt('my secret')
        open('/tmp/fasd', 'wb').write(x)
    else:  # otherwise decrypt
        # mess around with the ~/.ps_* files here...
        x = open('/tmp/fasd', 'rb').read()
        print(crypt(x, decrypt=True))
