import json
from web3 import Web3
from web3.middleware import geth_poa_middleware
from web3.exceptions import ContractLogicError

# Connect to local Ganache CLI
ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

# Add PoA middleware for compatibility with certain networks
web3.middleware_onion.inject(geth_poa_middleware, layer=0)

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

# Private key
private_key = "0x85118e3b6365c6230ea2340edb34553eb9084fd8b245260d8d7b66cf47050a14"
account_address = web3.eth.account.from_key(private_key).address

# Function to sign and send a transaction
def sign_and_send_transaction(tx):
    # Add transaction parameters
    tx['from'] = account_address
    tx['gas'] = 2000000
    tx['gasPrice'] = 20000000000  # Updated gas price
    # Sign the transaction
    signed_tx = web3.eth.account.sign_transaction(tx, private_key)
    # Send the transaction
    tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
    # Wait for the transaction receipt
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    return receipt

# Function to set a security key
def set_security_key(key):
    tx = contract.functions.setKey(key).build_transaction({
        'chainId': 1337,  # Chain ID for Ganache
        'nonce': web3.eth.get_transaction_count(account_address),
        'gas': 2000000,
        'gasPrice': 20000000000  # Updated gas price
    })
    receipt = sign_and_send_transaction(tx)
    print(f"Security key set: {key}, Transaction receipt: {receipt}")

# Function to get a security key for a user
def get_security_key(user_address):
    return contract.functions.getKey(user_address).call()

# Function to add an item to the inventory
def add_item(name, quantity):
    tx = contract.functions.addItem(name, quantity).build_transaction({
        'chainId': 1337,  # Chain ID for Ganache
        'nonce': web3.eth.get_transaction_count(account_address),
        'gas': 2000000,
        'gasPrice': 20000000000  # Updated gas price
    })
    receipt = sign_and_send_transaction(tx)
    print(f"Item added: {name}, Quantity: {quantity}, Transaction receipt: {receipt}")

# Function to update an item in the inventory
def update_item(id, name, quantity):
    tx = contract.functions.updateItem(id, name, quantity).build_transaction({
        'chainId': 1337,  # Chain ID for Ganache
        'nonce': web3.eth.get_transaction_count(account_address),
        'gas': 2000000,
        'gasPrice': 20000000000  # Updated gas price
    })
    receipt = sign_and_send_transaction(tx)
    print(f"Item updated: ID: {id}, Name: {name}, Quantity: {quantity}, Transaction receipt: {receipt}")

# Function to get item details
def get_item(id):
    item = contract.functions.getItem(id).call()
    return item

# Example usage
if __name__ == "__main__":
    try:
        # Set a security key
        set_security_key("my_secure_key")

        # Add an item to the inventory
        add_item("Item1", 100)

        # Update the item
        update_item(1, "Item1 Updated", 150)

        # Get the item details
        item = get_item(1)
        print(f"Item details: ID: {item[0]}, Name: {item[1]}, Quantity: {item[2]}")
    except ContractLogicError as e:
        print(f"An error occurred: {e}")
