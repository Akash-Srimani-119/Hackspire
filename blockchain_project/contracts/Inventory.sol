// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Inventory {
    struct Transaction {
        address from;
        address to;
        uint256 amount;
        uint256 timestamp;
    }

    Transaction[] public transactions;

    function createTransaction(address _to, uint256 _amount) public {
        transactions.push(Transaction(msg.sender, _to, _amount, block.timestamp));
    }

    function getTransaction(uint256 _id) public view returns (address, address, uint256, uint256) {
        Transaction memory transaction = transactions[_id];
        return (transaction.from, transaction.to, transaction.amount, transaction.timestamp);
    }

    function transactionCount() public view returns (uint256) {
        return transactions.length;
    }
}
