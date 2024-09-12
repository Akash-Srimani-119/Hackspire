import json
from web3 import Web3

# Connect to local Ganache CLI
ganache_url = "HTTP://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

# Check if connected to Ganache
print(f"Connected to Ethereum node: {web3.is_connected()}")

# Contract address and ABI (replace with your deployed contract address and ABI)
contract_address = "0x47C00bC565D211259CD0ec7Fb38e92Def2aa3D76"

contract_abi = json.loads("""
[
    {
        "inputs": [
            {
                "internalType": "string",
                "name": "_key",
                "type": "string"
            }
        ],
        "name": "setKey",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "_user",
                "type": "address"
            }
        ],
        "name": "getKey",
        "outputs": [
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "string",
                "name": "_name",
                "type": "string"
            },
            {
                "internalType": "uint256",
                "name": "_quantity",
                "type": "uint256"
            }
        ],
        "name": "addItem",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "_id",
                "type": "uint256"
            },
            {
                "internalType": "string",
                "name": "_name",
                "type": "string"
            },
            {
                "internalType": "uint256",
                "name": "_quantity",
                "type": "uint256"
            }
        ],
        "name": "updateItem",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "_id",
                "type": "uint256"
            }
        ],
        "name": "getItem",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            },
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            },
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    }
]
""")

# Create contract instance
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

# Set the default account (use one of the accounts provided by Ganache)
web3.eth.defaultAccount = web3.eth.accounts[0]

# Function to set a security key
def set_security_key(key):
    tx_hash = contract.functions.setKey(key).transact()
    web3.eth.waitForTransactionReceipt(tx_hash)
    print(f"Security key set: {key}")

# Function to get a security key for a user
def get_security_key(user_address):
    return contract.functions.getKey(user_address).call()

# Function to add an item to the inventory
def add_item(name, quantity):
    tx_hash = contract.functions.addItem(name, quantity).transact()
    web3.eth.waitForTransactionReceipt(tx_hash)
    print(f"Item added: {name}, Quantity: {quantity}")

# Function to update an item in the inventory
def update_item(id, name, quantity):
    tx_hash = contract.functions.updateItem(id, name, quantity).transact()
    web3.eth.waitForTransactionReceipt(tx_hash)
    print(f"Item updated: ID: {id}, Name: {name}, Quantity: {quantity}")

# Function to get item details
def get_item(id):
    item = contract.functions.getItem(id).call()
    return item

# Example usage
if __name__ == "__main__":
    # Set a security key
    set_security_key("my_secure_key")

    # Add an item to the inventory
    add_item("Item1", 100)

    # Update the item
    update_item(1, "Item1 Updated", 150)

    # Get the item details
    item = get_item(1)
    print(f"Item details: ID: {item[0]}, Name: {item[1]}, Quantity: {item[2]}")
