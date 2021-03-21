import uuid
import json
from backend.wallet import ellipticcurve
from backend.wallet import signatureGV
from cryptography.hazmat.backends import default_backend
import hashlib
def crypto_hash(*args):
   stringified_args=sorted(map(lambda data:json.dumps(data),args))
   
   joined_data=''.join(stringified_args)

   return hashlib.sha256(joined_data.encode('utf-8')).hexdigest()
class Wallet:
    def __init__(self):
      
       self.address=str(uuid.uuid4())[0:8]
       self.private_key=ellipticcurve.privKeyGeneration()
       self.public_key=ellipticcurve.EccMultiply(ellipticcurve.GPoint,self.private_key)
    
    def balance(self,transactionpool):
        return Wallet.calculate_balance(transactionpool,self.address)  
    def sign(self,data):
        hash_datahex = crypto_hash(data)
        hashval = int("0x"+hash_datahex, 16)
        sig = signatureGV.signature_generation(self.private_key,hashval)
        return sig
    
       
    @staticmethod
    def verify(public_key,data,signature):
        hash_datahex = crypto_hash(data)
        hashval = int("0x"+hash_datahex, 16)
        (r,s)=signature
        ver = signatureGV.signature_verification(public_key,r,s,hashval) 
        return ver
    @staticmethod
    def calculate_balance(transactionpool,address):
        balance=1000
        print("calculate balance")
        print(transactionpool.transaction_map)
        if not transactionpool.transaction_map:
            print("transaction pool true")
            return balance
        transactiondata=transactionpool.transaction_data()
       
        for transaction in transactiondata:
                if transaction['input']['address']==address:
                    balance=transaction['output'][address]
                elif address in transaction['output']:
                    balance+=transaction['output'][address]
        return balance 
   
def main():
    wallet=Wallet()
    print(f'wallet:{wallet.__dict__}')
    data={'foo':'bar'}
    signature=wallet.sign(data)
    print(f'signature:{signature}')
    should_be_valid=Wallet.verify(wallet.public_key,data,signature)
    print(f'should_be_valid:{should_be_valid}')
    should_be_invalid=Wallet.verify(Wallet().public_key,data,signature)
    print(f'should_be_invalid:{should_be_invalid}')
if __name__=='__main__':
    main()