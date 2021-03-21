import uuid
import time
from backend.wallet.wallet import Wallet
from backend.wallet.transaction_pool import TransactionPool
class Transaction:
    def __init__(self,sender_wallet=None,recipient=None,amount=None,transactionpool=None):
        print("initiating transaction")
        self.id= str(uuid.uuid4())[0:8]
        self.output= self.create_output(
            sender_wallet,
            recipient,
            amount,
            transactionpool
        )
        self.input=self.create_input(sender_wallet,self.output,transactionpool)
    def create_output(self,sender_wallet,recipient,amount,transactionpool):
        if amount>sender_wallet.balance(transactionpool):
            raise Exception('Amount exceeds balance')


        output={

        }
        output[recipient]=amount
        output[sender_wallet.address]=sender_wallet.balance(transactionpool)-amount
        return output
    def create_input(self,sender_wallet,output,transactionpool):
        return {
            'timestamp':time.time_ns(),
            'amount':sender_wallet.balance(transactionpool),
             'address':sender_wallet.address,
             'public_key':sender_wallet.public_key,
             'signature':sender_wallet.sign(output)

        }
   
    def to_json(self):
        return self.__dict__
    @staticmethod
    def from_json(transaction_json):
        return Transaction(**transaction_json
        )
    @staticmethod
    def is_valid_transaction(transaction):
        
        if not Wallet.verify(transaction.input['public_key'],transaction.output,transaction.input['signature']):
            raise Exception('Invalid signature')
   
def main():
    transaction=Transaction(Wallet(),'recipient',15)
    print(f'transaction.__dict__:{transaction.__dict__}')
if __name__=='__main__':
    main()