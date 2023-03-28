import socket
import json
from web3.auto import w3
from eth_account.messages import encode_defunct
from colorama import Fore

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65432        # The port used by the server



def sign_challenge(challenge, private_key):
    # Sign the challenge message with the private key
    message = encode_defunct(text=challenge)
    signed_message = w3.eth.account.sign_message(message, private_key=private_key)
    return signed_message.signature.hex()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print("Connected to slave robot.")

    # Receive the challenge from the server
    challenge = s.recv(1024).decode()
    print("Received challenge:", challenge)

    print(Fore.YELLOW + '\033[1m' + 'Test key: 0x50172b5ea82c075621a1eba0419f757ee9f31f39abc4f06a1b6fc996c6e46311' + '\033[0m')
    print(Fore.GREEN + '\033[1m' + 'SURGEON AUTHENTICATION' + '\033[0m')
    private_key = input('Enter the surgeon private key: ')

    signature = sign_challenge(challenge, private_key)

    # Send the signed challenge back to the server
    s.sendall(signature.encode())

    # Receive the authentication result from the server
    result = s.recv(1024).decode()
    print(result)
