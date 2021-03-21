import os
import random
import requests
from flask import Flask,jsonify,request
from flask_cors import CORS,cross_origin

from backend.wallet.wallet import Wallet
from backend.wallet.transaction import Transaction
from backend.wallet.transaction_pool import TransactionPool

app=Flask(__name__)
CORS(app,resources={r'/*':{'origins':'http://localhost:3000'}})

wallet=Wallet()
transactionpool=TransactionPool()

print(wallet)
@app.route('/')
def route_default():
    return 'Welcome to the blockchain'

ROOT_PORT=5000



@app.route('/wallet/transact',methods=['POST'])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def route_wallet_transact():
    
    transaction_data=request.get_json()
    
    transaction=Transaction(wallet,transaction_data['recipient'],transaction_data['amount'],transactionpool)
    print(f'transaction.to_json():{transaction.to_json()}')
    transactionpool.set_transaction(transaction)
    return jsonify(transaction.to_json())



@app.route('/wallet/info')
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def route_wallet_info():
    return jsonify({'address':wallet.address,'balance':wallet.balance(transactionpool)})

# @app.route('/known-addresses')
# @cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
# def route_known_addresses():
#     known_addresses=set();
#     for block in blockchain.chain:
#         for transaction in block.data:
            
#             known_addresses.update(transaction['output'].keys())
#     return jsonify(list(known_addresses))

@app.route('/transactions')
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def route_transactions():
    print(transactionpool.transaction_data())
    return jsonify(transactionpool.transaction_data())

PORT=ROOT_PORT


app.run(port=PORT)
