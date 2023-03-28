from web3 import Web3
from eth_account.messages import encode_defunct
from web3.auto import w3
import datetime
import json
import socket
import uuid
import colorama
from colorama import Fore

# Connect to Ganache
ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

# Replace with your address
user_address = "0x52CfF12eae83154d665011E493B144265E0385BE"
private_key = "0x15f75d6216ae540382e63bd64cb4844f4d552783a7e3af255fada68dacb7361b"
user_contracts = []
surgeon_identity = ""
remote_control = False # Variable to verify of remote control has been granted to master console or not

#The ABI is saved in a file named abi.json
with open('abi.json', 'r') as f:
    abi = json.load(f)

def get_all_user_contracts():
    user_contracts.clear()
    # Get all the blocks in the blockchain
    blockchain_length = web3.eth.block_number
    for i in range(blockchain_length + 1):
        block = web3.eth.get_block(i, full_transactions=True)
        transactions = block['transactions']
        for tx in transactions:
            tx_receipt = web3.eth.get_transaction_receipt(tx['hash'])
            if tx_receipt.contractAddress is not None:
                if tx_receipt['from'] == user_address:
                    contract_address = tx_receipt.contractAddress
                    contract = web3.eth.contract(address=contract_address, abi=abi)
                    print(f"Contract created by {user_address} at block number {i}:")
                    print(datetime.datetime.fromtimestamp(block.timestamp)) #Timestamp block was created
                    print(contract.functions.getConsentDetails().call())
                    print("Contract address:", contract_address)
                    user_contracts.append(contract_address) # Append contract address to the list
                    print()

def extract_surgeon_identity(contract_address):
    contract = web3.eth.contract(address=contract_address, abi=abi)
    # Print the contract details
    print("Selected Contract Address:", contract_address)
    contract_details = contract.functions.getConsentDetails().call()
    surgeon_identity = contract_details[4]
    print("Contract Details:", contract_details)
    return surgeon_identity

def sign_challenge(challenge, private_key):
    # Sign the challenge message with the private key
    message = encode_defunct(text=challenge)
    signed_message = w3.eth.account.sign_message(message, private_key=private_key)
    return signed_message.signature.hex()

def authenticate_surgeon(conn, surgeon_address):
    # Generate a random challenge and send it to the client
    nonce = nonce = uuid.uuid4().hex
    challenge = "Please sign this challenge: " + nonce
    #print(challenge)
    conn.sendall(challenge.encode())

    # Receive the signed challenge from the client
    signature = conn.recv(1024).decode()
    
    # Verify the signature using the client's public address
    message = encode_defunct(text=challenge)
    verified_address = w3.eth.account.recover_message(message, signature=signature)
    
    if verified_address.lower() == surgeon_address.lower():
        print(Fore.GREEN + '\033[1m' + 'Surgeon authentication successful.' + '\033[0m')
        # Grant remote control to the master console
        remote_control = True
        conn.sendall("Authentication successful.\n".encode())
        print(Fore.GREEN + '\033[1m' + 'Remote control granted to the master console.\nAll authentication steps have been completed, and the surgery is about to begin...'  + '\033[0m')
        conn.sendall("Remote control granted.".encode())
        # Some function to handle the rest of the surgical process
    else:
        print(Fore.RED + '\033[1m' + 'Surgeon authentication failed.'  + '\033[0m')
        conn.sendall("Authentication failed.".encode())
    
def open_socket():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print('Server listening on', (HOST, PORT))
        while True:
            conn, addr = s.accept()
            with conn:
                print('Client connected:', addr)
                # Authenticate the surgeon with public address
                authenticate_surgeon(conn, surgeon_identity)

# Authenticate account
account = web3.eth.account.from_key(private_key)
if account.address.lower() == user_address.lower():
    print("Authentication successful")
    get_all_user_contracts()
    
    # Prompt user to select a contract
    contract_address = input(Fore.GREEN + '\033[1m' + 'Enter the address of the contract you wish to execute\n' + '\033[0m')
    
    # Verify that the authenticated user created the contract
    try:
        if contract_address in user_contracts:
            surgeon_identity = extract_surgeon_identity(contract_address)
            print("Surgeon Identity: " + surgeon_identity)
            # open socket to listen to connection from the master console
            # Authenticate the master console
            print("Waiting for the surgeon to connect and authenticate...")
            open_socket()
        else:
            print(Fore.RED + '\033[1m' + 'Invalid contract selected' + '\033[0m')
    except ValueError:
        print("That item does not exist")     

else:
    print("Authentication unsuccessful")
