from web3 import Web3
import json

# Connect to Ganache
ganache_url = "HTTP://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

if web3.is_connected():
    print("Connected to Ganache")
else:
    print("Failed to connect to Ganache")

# Set default account
web3.eth.default_account = web3.eth.accounts[0]

# ABI and contract address (replace with your own)
abi = json.loads('''[
    {
        "constant": false,
        "inputs": [
            {
                "name": "_trackingId",
                "type": "string"
            },
            {
                "name": "_status",
                "type": "string"
            }
        ],
        "name": "updateStatus",
        "outputs": [],
        "payable": false,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": true,
        "inputs": [
            {
                "name": "_trackingId",
                "type": "string"
            }
        ],
        "name": "getStatus",
        "outputs": [
            {
                "name": "",
                "type": "string"
            }
        ],
        "payable": false,
        "stateMutability": "view",
        "type": "function"
    }
]''')

contract_address = "0x4e45bDEdB387a7ac574C9864E3d0E6810cCc2968"

# Interact with the contract
contract = web3.eth.contract(address=contract_address, abi=abi)

def update_status(tracking_id, status):
    tx_hash = contract.functions.updateStatus(tracking_id, status).transact()
    web3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Updated status for {tracking_id} to {status}")

def get_status(tracking_id):
    status = contract.functions.getStatus(tracking_id).call()
    print(f"Status for {tracking_id}: {status}")
    return status

# Example usage
update_status("12345", "In Transit")
get_status("12345")
