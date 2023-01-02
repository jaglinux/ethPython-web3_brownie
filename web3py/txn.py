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

def save_obj(data, file_name, flag):
    assert flag in ['w', 'a']
    data = Web3.toJSON(data)
    data = json.loads(data)
    try:
        with open(file_name, flag) as f:
            f.write(json.dumps(data, indent=4))
    except Exception as ex:
        print("data save failed", ex)

def read_obj(file_name):
    data = None

    try:
        with open(file_name, "r") as f:
            data = json.loads(f.read())
    except Exception as ex:
        print("data read failed", ex)
    
    return data

@check_if_connected
def create_new_account():
    new_acct = w3.eth.account.create()
    print(new_acct)

@check_if_connected
def get_latest_block():
    block = w3.eth.get_block('latest')
    #block = {block['number']:block}
    save_obj(block, "block.json", 'w')

def get_saved_block():
    data = read_obj("block.json")
    if data is None:
        print("No history")
    else:
        print(data, type(data), len(data))

def get_transactions_hashes():
    data = read_obj("block.json")
    print(data)
    if data is None:
        print("No history")
    else:  
        txns_hashes = data['transactions']
        print("transaction hashes are ", txns_hashes)
        print("Number of txn hashes are ", len(txns_hashes))
        save_obj(txns_hashes, "txns.json", "w")

@check_if_connected
def parse_txn():
    txns_hashes = read_obj("txns.json")
    print("Number of transactions ", txns_hashes)
    txn_file = read_obj("txn.json")
    if txn_file is None:
        txn_file = {}
    new_txn_file = {}
    for i, txn_hash in enumerate(txns_hashes):
        #print("txn_hash ------ ", txn_file.get(txn_hash))
        txn = w3.eth.get_transaction_receipt(txn_hash)
        #print(f"Transaction {i} : {txn} ")
        print("---------- Interacted with contract ", txn['to'])
        print("-------------------------------------------------")
        new_txn_file[txn['to']] = True
    print("-----------", new_txn_file)
    if new_txn_file:
        txn_file.update(new_txn_file)
        print("----------SAVING")
        save_obj(txn_file, "txn.json", 'w')

if __name__ == "__main__":
    print("Enter 0 to read latest block")
    print("Enter 1 to read block from previous store")
    print("Enter 2 to read transactions from saved block")
    print("Enter 3 to parse transactions from saved block")
    print("Enter any other key to EXIT...")
    while True:
        in1 = int(input())
        if in1 == 0:
            get_latest_block()
        elif in1 == 1:
            get_saved_block()
        elif in1 == 2:
            get_transactions_hashes()
        elif in1 == 3:
            parse_txn()
        else:
            break
        print("Awaiting next input...")
