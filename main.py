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
            f.write(text.decode())
    except FileNotFoundError:
        print("File not found")
        exit()

def encrypt_action():
    filename = input("Filename: ")

    question1 = input("Generate key? (y/n): ")

    if(question1 == "y"):
        encrypt_key = jacklib_createpwd()
        print("Key: " + encrypt_key.decode())
    elif (question1 == "n"):
        encrypt_key = input("Key: ")
    else:
        print("Invalid input")
        exit()

    question2 = input("Encrypt? (y/n): ")

    if(question2 == "y"):
        try:
            data = jacklib_SHA256(get_text(filename).encode(), encrypt_key)
        except:
            data = jacklib_SHA256(get_text(filename), encrypt_key)
        print("Encrypted!")
        write_text(filename, data[0])
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
        try:
            data = jacklib_SHA256_Decode(get_text(filename).encode(), encrypt_key)
        except:
            data = jacklib_SHA256_Decode(get_text(filename), encrypt_key)
        write_text(filename, data)
        print("Decrypted!")
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