import base64
import pyperclip
from jacklib import *

'''
encrypt_key = jacklib_createpwd()

data = jacklib_SHA256(text.encode(), encrypt_key)
'''

print("""
\n
Actions available:
1. Encrypt
2. Decrypt
\n\n
""")

def get_file_size(filename):
    try:
        with open(filename, 'rb') as f:
            return len(f.read())
    except FileNotFoundError:
        print("File not found")
        exit()

def get_text(filename):
    try:
        with open(filename, 'rb') as f:
            text = f.read()
            return text
    except FileNotFoundError:
        print("File not found")
        exit()

def write_text(filename, text):
    try:
        with open(filename, 'wb') as f:
            try:
                f.write(text)
            except:
                f.write(text.encode())
    except FileNotFoundError:
        print("File not found")
        exit()

def encrypt_action():
    filename = input("Filename: ")

    question1 = input("Generate key? (y/n): ")

    if(question1 == "y"):
        encrypt_key = jacklib_createpwd()
        print("Key: " + encrypt_key.decode())

        pyperclip.copy(encrypt_key.decode())
        print("Key copied to clipboard\n")

    elif (question1 == "n"):
        encrypt_key = input("Key: ")
    else:
        print("Invalid input")
        exit()

    question2 = input("Encrypt? (y/n): ")

    if(question2 == "y"):
        try:
            b64data = base64.b64encode(get_text(filename))
            data = jacklib_SHA256(b64data.encode(), encrypt_key)
        except:
            b64data = base64.b64encode(get_text(filename))
            data = jacklib_SHA256(b64data, encrypt_key)
        beforesize = get_file_size(filename)
        write_text(filename, data[0])
        aftersize = get_file_size(filename)
        print(f"Encrypted! ({beforesize} -> {aftersize})")
    elif (question2 == "n"):
        print("Aborted")
        exit()
    else:
        print("Invalid input")
        exit()

def decrypt_action():
    filename = input("Filename: ")
    encrypt_key = input("Key: ").encode()
    question1 = input("Decrypt? (y/n): ")

    if(question1 == "y"):
        base64data = jacklib_SHA256_Decode(get_text(filename), encrypt_key)

        dbase64data = base64.b64decode(base64data)
        beforesize = get_file_size(filename)
        write_text(filename, dbase64data)
        aftersize = get_file_size(filename)
        print(f"Decrypted! ({beforesize} -> {aftersize})")
    elif (question1 == "n"):
        print("Aborted")
        exit()
    else:
        print("Invalid input")
        exit()

action = input("Action: ")

if(action == "1"):
    encrypt_action()
elif (action == "2"):
    decrypt_action()
else:
    print("Invalid input")
    exit()