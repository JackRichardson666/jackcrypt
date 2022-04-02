'''


   d8b                   888      888 d8b 888      
   Y8P                   888      888 Y8P 888      
                         888      888     888      
  8888  8888b.   .d8888b 888  888 888 888 88888b.  
  "888     "88b d88P"    888 .88P 888 888 888 "88b 
   888 .d888888 888      888888K  888 888 888  888 
   888 888  888 Y88b.    888 "88b 888 888 888 d88P 
   888 "Y888888  "Y8888P 888  888 888 888 88888P"  
   888                                             
  d88P                                             
888P"                                              

Copyright© - Jack Richardson

License - GNU (https://www.gnu.org/licenses/gpl-3.0.ru.html)

API'S -
PyCryptodome: https://pycryptodome.readthedocs.io/
cryptography: https://cryptography.io/en/latest/

Me -
 YouTube: https://www.youtube.com/channel/UCde3DmggZl7D9dZG-DVvCDw

About -

 This library, if you can call it that, is designed to simplify the use of certain encryption methods.

 Here you can find a small number of encryption methods such as: SHA256, AES, DES

 This library is friendly with sockets, based on it you can create a symmetric method of communication with Server -> Client or vice versa Client -> Server(reverse socket)

 The most convenient and secure method of this library is SHA256

 You can change the hash method from SHA256 to any other method (from jacklib_SHA256)

PLEASE READ THIS!!!!!
 ~Я прекрасно знаю, что этот код очень плох в реализации и может быть сокращен во много раз, но поскольку это моя первая общедоступная библиотека, пожалуйста, не судите меня строго и не выливайте на меня чан с дерьмом ^^
 ~I know perfectly well that this code is very bad to implement and could be cut down many times, but since this is my first shared library, please don't judge me harshly and don't pour a layer of shit on me ^^

 ~Пожалуйста, оставьте авторские права на меня и мою библиотеку, и я также попрошу Вас не использовать jacklib для вредоносных и корыстных целей (вирусы, ботнеты, трояны и аналогичные вредоносные программы)
 ~Please leave the copyright on me and my library, and I will also ask you not to use jacklib for malicious and self-serving purposes (viruses, botnets, Trojans, and similar malicious programs)

Made with love by Jack Richardson ❤
'''

#some imports
import os
import json
import base64
import hashlib
import random
import string
import secrets

#cryptography
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

#PyCryptodome
from Crypto.Cipher import AES
from Crypto.Hash import SHA
from Crypto.Cipher import DES
from Crypto import Random
from Crypto.Random import get_random_bytes

#random string aka pwd gen
def jacklib_random_string(stringLength):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

#pad text
def jacklib_pad(text):
    n = len(text) % 8
    return text + (b' ' * n)

#create password
def jacklib_createpwd():
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=os.urandom(24),
        iterations=100000,
        backend=default_backend())
    key_genned = base64.urlsafe_b64encode(kdf.derive(jacklib_random_string(16).encode()))
    return key_genned

#SHA256
def jacklib_SHA256(text, created_key):
    return Fernet(created_key).encrypt(text), created_key

def jacklib_SHA256_Decode(encrypted, key):
    return Fernet(key).decrypt(encrypted.decode())

#AES
def jacklib_AES(text, password):
    salt = get_random_bytes(AES.block_size)
    private_key = hashlib.scrypt(
        password.encode(), salt=salt, n=2**14, r=8, p=1, dklen=32)

    cipher_config = AES.new(private_key, AES.MODE_GCM)
    cipher_text, tag = cipher_config.encrypt_and_digest(bytes(text, 'utf-8'))
    return {
        'cipher_text': base64.b64encode(cipher_text).decode('utf-8'),
        'salt': base64.b64encode(salt).decode('utf-8'),
        'nonce': base64.b64encode(cipher_config.nonce).decode('utf-8'),
        'tag': base64.b64encode(tag).decode('utf-8')
    }

def jacklib_AES_Decode(text, password):
    salt = base64.b64decode(text['salt'])
    cipher_text = base64.b64decode(text['cipher_text'])
    nonce = base64.b64decode(text['nonce'])
    tag = base64.b64decode(text['tag'])

    private_key = hashlib.scrypt(
        password.encode(), salt=salt, n=2**14, r=8, p=1, dklen=32)

    cipher = AES.new(private_key, AES.MODE_GCM, nonce=nonce)
    decrypted = cipher.decrypt_and_verify(cipher_text, tag)
    return decrypted

#DES
def jacklib_DES(text):
    key = secrets.token_bytes(8)
    cipher = DES.new(key, DES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(text.encode('ascii'))
    return nonce, ciphertext, tag, key

def jacklib_DES_Decode(nonce, ciphertext, tag, key):
    cipher = DES.new(key, DES.MODE_EAX, nonce=nonce)
    plaintext = cipher.decrypt(ciphertext)

    try:
        cipher.verify(tag)
        return plaintext.decode('ascii')
    except:
        return False