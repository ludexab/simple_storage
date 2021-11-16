from solcx import compile_standard
import json
from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()
"""
In order to deploy a smart contract,
1. create a compile object with necessary arguments,
2. dump the compile object to a .json file
3. get the bytecode
4. get the ABI
5. connect to a local blockchain server e.g Ganache using web3
6. get the chainId
7. get the blockchain address
8. get the private key to the address
9. create the smart contract in python using web3 object created in (5)
10. get the nonce/latest transaction using web3 created in (5)
11. Build a transaction with the contract created in (9)
12. Sign the transaction created in (11) with the web3 obj in (5) and private key in (8)
13. Send the transaction signed in (12) using web3 obj in (5)
14. wait for the sent transaction receipt sent in (13)

"""

with open("./SimpleStorage.sol", "r") as file:
    simpleStorage = file.read()

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simpleStorage}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.6.0",
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# get ABI
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# connecting to ganache
w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))
chain_id = 1337
my_address = "0x9C1f97a47534Ac7FC483e92a8Ab8F8C4F7394232"
private_key = os.getenv("PRIVATE_KEY")

# create the contract in python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# get nonce/ the latest transaction
nonce = w3.eth.getTransactionCount(my_address)

# To deploy a contract, we basically:
# 1. Build a transaction
# 2. Sign a transaction
# 3. Send a transaction

# 1
transaction = SimpleStorage.constructor().buildTransaction(
    {"chainId": chain_id, "from": my_address, "nonce": nonce}
)

# 2
signedTransaction = w3.eth.account.sign_transaction(
    transaction, private_key=private_key
)

# 3
txn_hash = w3.eth.send_raw_transaction(signedTransaction.rawTransaction)
txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)
