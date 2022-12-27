from web3 import Web3
import os
GANACHE_URL = 'HTTP://127.0.0.1:7545'
INFURIA_URL = 'https://mainnet.infura.io/v3/<private>'

blockchain = os.environ['CHAIN']
print('blockchain selected is ', blockchain)
url = ''
if blockchain == 'MAIN':
    url = INFURIA_URL
elif blockchain == 'LOCAL':
    url = GANACHE_URL
else:
    raise Exception('no blockchain selected')

web3 = Web3(Web3.HTTPProvider(url))
print('web3 is connected ', web3.isConnected(), ' for', blockchain)
print('block number is ', web3.eth.blockNumber)

def create_payment_txn(nonce, dest_addr, eth, gas, gasPrice):
    return {'nonce':nonce, 'to': dest_addr, 'value':web3.toWei(eth, 'ether'), 'gas':gas, 'gasPrice':web3.toWei(gasPrice, 'gwei')}

def sign_txn(txn, key):
    return web3.eth.account.signTransaction(txn, key)

def send_txn(signed_txn):
    hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
    return web3.toHex(hash)

def main_blockchain():
    balance = web3.eth.getBalance('<private>')
    balance = web3.fromWei(balance, 'ether')
    print('my balance is ', balance)

    contract_abi = '[{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_value","type":"uint256"}],"name":"approve","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transferFrom","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"},{"name":"_data","type":"bytes"}],"name":"transferAndCall","outputs":[{"name":"success","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_subtractedValue","type":"uint256"}],"name":"decreaseApproval","outputs":[{"name":"success","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[{"name":"success","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_addedValue","type":"uint256"}],"name":"increaseApproval","outputs":[{"name":"success","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"},{"name":"_spender","type":"address"}],"name":"allowance","outputs":[{"name":"remaining","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"name":"from","type":"address"},{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"value","type":"uint256"},{"indexed":false,"name":"data","type":"bytes"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"owner","type":"address"},{"indexed":true,"name":"spender","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Approval","type":"event"}]'
    contract_address = '0x514910771af9ca656af840dff83e8264ecf986ca'

    contract_address = Web3.toChecksumAddress(contract_address)
    contract = web3.eth.contract(address=contract_address, abi=contract_abi)
    token_balance = contract.functions.totalSupply().call()
    print('token symbol is ', contract.functions.symbol().call())
    print('token balance is ', web3.fromWei(token_balance, 'ether'))

def local_blockchain():
    addr_1 = '0xdbcC23c3196101DA306386a4651628AfA00B8ab5'
    addr_1_key = '512d28f35892058382095a417710549e962998e5e9f90ccbfde44135f32ed428'
    addr_2 = '0x4013488bc377A5Dd631fa5cEC7Ca5C9cBf652C44'

    nonce = web3.eth.getTransactionCount(addr_1)
    print('nonce is ', nonce)
    txn = create_payment_txn(nonce, addr_2, 0.5, 2000000, 50)
    txn = sign_txn(txn, addr_1_key)
    hash = send_txn(txn)
    print(hash)

if blockchain == 'MAIN':
    main_blockchain()
else:
    local_blockchain()
