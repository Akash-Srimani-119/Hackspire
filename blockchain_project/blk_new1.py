import hashlib
import time
import json
from cryptography.fernet import Fernet
import base64

class Block:
    def __init__(self, index, previous_hash, timestamp, data, nonce=0):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.nonce = nonce
        self.hash = self.calculate_hash()
    
    def calculate_hash(self):
        block_data = {
            "index": self.index,
            "previous_hash": self.previous_hash,
            "timestamp": self.timestamp,
            "data": self.data,
            "nonce": self.nonce
        }
        block_string = json.dumps(block_data, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()
    
    def __str__(self):
        block_data = {
            "index": self.index,
            "previous_hash": self.previous_hash,
            "timestamp": self.timestamp,
            "data": self.data,
            "nonce": self.nonce,
            "hash": self.hash
        }
        return json.dumps(block_data, sort_keys=True, indent=4)

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 4
        self.pending_transactions = []
        self.mining_reward = 100
        self.key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.key)
    
    def create_genesis_block(self):
        return Block(0, "0", time.time(), "Genesis Block")
    
    def get_latest_block(self):
        return self.chain[-1]
    
    def mine_pending_transactions(self, mining_reward_address):
        new_block = Block(len(self.chain), self.get_latest_block().hash, time.time(), self.pending_transactions)
        new_block = self.proof_of_work(new_block)
        self.chain.append(new_block)
        self.pending_transactions = [
            {"from": None, "to": mining_reward_address, "amount": self.mining_reward}
        ]
    
    def add_transaction(self, sender, recipient, amount):
        if not sender or not recipient or not amount:
            raise ValueError("Transaction must include sender, recipient, and amount")
        
        encrypted_transaction = self.encrypt_transaction(sender, recipient, amount)
        self.pending_transactions.append(encrypted_transaction)
    
    def encrypt_transaction(self, sender, recipient, amount):
        transaction = json.dumps({
            "sender": sender,
            "recipient": recipient,
            "amount": amount
        }).encode()
        
        encrypted_transaction = self.cipher_suite.encrypt(transaction)
        return base64.urlsafe_b64encode(encrypted_transaction).decode()
    
    def proof_of_work(self, block):
        while block.hash[:self.difficulty] != "0" * self.difficulty:
            block.nonce += 1
            block.hash = block.calculate_hash()
        return block
    
    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]
            
            if current_block.hash != current_block.calculate_hash():
                return False
            
            if current_block.previous_hash != previous_block.hash:
                return False
        
        return True

class Store:
    def __init__(self, store_id):
        self.store_id = store_id
        self.orders = []
    
    def place_order(self, blockchain, recipient, amount):
        blockchain.add_transaction(self.store_id, recipient, amount)
        self.orders.append({
            "recipient": recipient,
            "amount": amount
        })

# Example usage
if __name__ == "__main__":
    # Initialize the blockchain
    my_blockchain = Blockchain()

    # Create stores
    store_a = Store("Store_A")
    store_b = Store("Store_B")

    # Stores place orders
    store_a.place_order(my_blockchain, "Supplier_X", 150)
    store_b.place_order(my_blockchain, "Supplier_Y", 300)
    store_a.place_order(my_blockchain, "Supplier_Z", 200)

    # Mine pending transactions
    print("Starting the miner...")
    my_blockchain.mine_pending_transactions("Miner1")

    # Validate the blockchain
    print("Blockchain valid?", my_blockchain.is_chain_valid())

    # Print the blockchain
    for block in my_blockchain.chain:
        print(block)
    
    # Print store orders
    print("Store A Orders:", store_a.orders)
    print("Store B Orders:", store_b.orders)
