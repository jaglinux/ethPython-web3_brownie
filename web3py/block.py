from web3 import Web3
import os
import json

w3 = None

def connect_to_web3():
    infura_http = os.environ['INFURA']
    global w3
    w3 = Web3(Web3.HTTPProvider(infura_http))
    print("Web3 is now conected ", w3.isConnected())

def check_if_connected():
    if w3 is None:
        print("Web3 not connected... ")
        connect_to_web3()

def create_new_account():
    check_if_connected()
    new_acct = w3.eth.account.create()
    print(new_acct)

def get_latest_block():
    check_if_connected()
    block = w3.eth.get_block('latest')
    save_obj(block, "block.data")

def get_latest_block_number():
    check_if_connected()
    block = w3.eth.get_block('latest')
    save_obj(block, "block.data")
    print(block['number'])

def get_saved_block():
    data = read_obj("block.data")
    if data is None:
        print("No history")
    else:
        print(data)

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

if __name__ == "__main__":
    print("Enter 0 to read latest block")
    print("Enter 1 to read latest block number")
    print("Enter 2 to read block from previous store")
    print("Enter any other key to EXIT...")
    while True:
        in1 = int(input())
        if in1 == 0:
            get_latest_block()
        elif in1 == 1:
            get_latest_block_number()
        elif in1 == 2:
            get_saved_block()
        else:
            break
        print("Awaiting next input...")
