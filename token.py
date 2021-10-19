#!/usr/bin/python3

from brownie import Token, accounts, config, Contract

class token():
    def __init__(self, addr):
        self.c = addr
        self.decimal = self.c.decimals()

    def getBalanceOf(self, addr):
        balance = self.c.balanceOf(addr)
        return balance/(10 ** self.decimal)
    
    def transfer(self, to, amount, source):
        self.c.transfer(to, amount * (10 ** 18), {'from':source})

def main():
    account = accounts.add(config['wallets']['from_key'])
    #Rinkeby
    c = Contract.from_explorer("0x9bf0a3A741a71A33209CA54ec944DFFCD1D72887")
    t = token(c)
    print(t.getBalanceOf(account))
    t.transfer(<Enter dest address>, 0.1, account)
