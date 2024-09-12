import hashlib
import json
import datetime

class Transaction:
  def __init__(self, sender_store, receiver_store, items, timestamp):
    self.sender_store = sender_store
    self.receiver_store = receiver_store
    self.items = items
    self.timestamp = timestamp

def hash_transaction(transaction):
  data = transaction.__dict__
  data_string = json.dumps(data, sort_keys=True)
  return hashlib.sha256(data_string.encode()).hexdigest()

class Block:
  def __init__(self, transactions, previous_hash):
    self.transactions = transactions
    self.previous_hash = previous_hash
    self.hash = self.calculate_hash()

  def calculate_hash(self):
    data = {
      "transactions": self.transactions,
      "previous_hash": self.previous_hash
    }
    data_string = json.dumps(data, sort_keys=True)
    return hashlib.sha256(data_string.encode()).hexdigest()

class Blockchain:
  def __init__(self):
    self.chain = [self.create_genesis_block()]

  def create_genesis_block(self):
    return Block([], "0")  # Genesis block has no previous hash

  def get_latest_block(self):
    return self.chain[-1]

  def add_block(self, block):
    self.chain.append(block)

  # Example usage
  def create_transaction(self, sender_store, receiver_store, items):
    transaction = Transaction(sender_store, receiver_store, items, str(datetime.datetime.now()))
    transaction_hash = hash_transaction(transaction)
    return transaction, transaction_hash

  def create_new_block(self, transactions):
    previous_block = self.get_latest_block()
    previous_hash = previous_block.hash
    new_block = Block(transactions, previous_hash)
    return new_block

# Example usage
if __name__ == "__main__":
  my_chain = Blockchain()

  # Create some transactions
  transaction_1, transaction_hash_1 = my_chain.create_transaction("Store A", "Store B", ["10 boxes of Pencils", "5 Notebooks"])
  transaction_2, transaction_hash_2 = my_chain.create_transaction("Store B", "Store C", ["2 Laptops", "1 Printer"])

  # Create a new block with the transactions
  block = my_chain.create_new_block([transaction_1, transaction_2])

  # Add the block to the chain
  my_chain.add_block(block)

  print("Our Blockchain:")
  for block in my_chain.chain:
    print(f"Hash: {block.hash}")
    print(f"Previous Hash: {block.previous_hash}")
    print(f"Transactions:")
    for transaction in block.transactions:
      print(f"- Sender: {transaction.sender_store}")
      print(f"  Receiver: {transaction.receiver_store}")
      print(f"  Items: {transaction.items}")
      print("---")
    print("----------")
