from web3 import Web3
import os
import json

w3 = None

def connect_to_web3():
    infura_http = os.environ['INFURA']
    global w3
    w3 = Web3(Web3.HTTPProvider(infura_http))
    print("Web3 is now conected ", w3.isConnected())

def check_if_connected(func):
    def wrapper():
        if w3 is None:
            print("Web3 not connected... ")
            connect_to_web3()
        func()
    return wrapper

@check_if_connected
def create_new_account():
    new_acct = w3.eth.account.create()
    print(new_acct)

@check_if_connected
def get_latest_block():
    block = w3.eth.get_block('latest')
    save_obj(block, "block.data")

@check_if_connected
def get_latest_block_number():
    block = w3.eth.get_block('latest')
    save_obj(block, "block.data")
    print(block['number'])

def get_saved_block():
    data = read_obj("block.data")
    if data is None:
        print("No history")
    else:
        print(data)


def get_transactions_hashes():
    data = read_obj("block.data")
    if data is None:
        print("No history")
    else:  
        txns_hashes = data['transactions']
        print("transaction hashes are ", txns_hashes)
        print("Number of txn hashes are ", len(txns_hashes))
        save_obj(txns_hashes, "txns.data")

def save_obj(data, file_name):
    data = Web3.toJSON(data)

    try:
        with open(file_name, "w") as f:
            f.write(data)
    except Exception as ex:
        print("data save failed", ex)

def read_obj(file_name):
    data = None

    try:
        with open(file_name, "r") as f:
            data = json.load(f)
    except Exception as ex:
        print("data read failed", ex)
    
    return data

@check_if_connected
def print_txn():
    txns_hashes = read_obj("txns.data")
    print("Number of transactions ", len(txns_hashes))
    for i, txn_hash in enumerate(txns_hashes):
        txn = w3.eth.get_transaction_receipt(txn_hash)
        print(f"Transaction {i} : {txn} ")
        print("---------- Interacted with contract ", txn['to'])
        print("-------------------------------------------------")
    

if __name__ == "__main__":
    print("Enter 0 to read latest block")
    print("Enter 1 to read latest block number")
    print("Enter 2 to read block from previous store")
    print("Enter 3 to read transactions from saved block")
    print("Enter 4 to parse transactions from saved block")
    print("Enter any other key to EXIT...")
    while True:
        in1 = int(input())
        if in1 == 0:
            get_latest_block()
        elif in1 == 1:
            get_latest_block_number()
        elif in1 == 2:
            get_saved_block()
        elif in1 == 3:
            get_transactions_hashes()
        elif in1 == 4:
            print_txn()
        else:
            break
        print("Awaiting next input...")
