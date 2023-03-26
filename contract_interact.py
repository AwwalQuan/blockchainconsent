from web3 import Web3
import datetime
import json
import colorama
from colorama import Fore

# Connect to Ganache
ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

# Replace with your address
user_address = "0x52CfF12eae83154d665011E493B144265E0385BE"
private_key = "0x15f75d6216ae540382e63bd64cb4844f4d552783a7e3af255fada68dacb7361b"
user_contracts = []
surgeon_identity = ""

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
        else:
            print(Fore.RED + '\033[1m' + 'Invalid contract selected' + '\033[0m')
    except ValueError:
        print("That item does not exist")     

else:
    print("Authentication unsuccessful")
