#javascript (push() , pop())    Python(append(), pop())
from itertools import chain
import functools
import json
import pickle
from collections import OrderedDict
from hash_util import hash_string_256, hash_block


MINING_REWARD=10
genesis_block={
        "previous_hash":"",
        "index":0,
        "transactions":[],
        'proof':100
}
blockchain=[]
open_transactions=[]
owner="Taimoor Haider"
participants={"Taimoor Haider"}


def load_data():
    global blockchain
    global open_transactions
    try:
      with open("blockchain.txt",mode='r') as f:
         file_content=f.readlines()
         # file_content=pickle.loads(f.read())
    
         # blockchain=file_content['chain']
         # open_transactions=file_content['ot']
         blockchain=json.loads(file_content[0][:-1])
         updated_blockchain=[]
         for block in blockchain:
             updated_block={
                 'previous_hash':block['previous_hash'],
                 'index':block['index'],
                 'proof':block['proof'],
                 'transactions':[OrderedDict([('sender',tx['sender']),('recipient',tx['recipient']),('amount',tx['amount'])]) for tx in block['transactions']]
             } 
             updated_blockchain.append(updated_block)
         blockchain=updated_blockchain
         open_transactions=json.loads(file_content[1])
         updated_transactions=[]
         for tx in open_transactions:
             updated_transaction=[OrderedDict([('sender',tx['sender']),('recipient',tx['recipient']),('amount',tx['amount'])])]
             updated_blockchain.append(updated_transaction)
         open_transactions=updated_transactions  
    except IOError:
            MINING_REWARD=10
            genesis_block={
             "previous_hash":"",
             "index":0,
             "transactions":[],
             'proof':100
            }
            blockchain=[genesis_block]

load_data()

def save_data():
    try:
       with open("blockchain.txt",mode='w') as f:
          f.write(json.dumps(blockchain))
          f.write('\n')
          f.write(json.dumps(open_transactions))
          # save_data={
          #     'chain':blockchain,
          #     'ot':open_transactions
          # }
          # f.write(pickle.dumps(save_data))

    except IOError:
        print("Failed to save!")


def get_last_blockchain_element():
    if(len(blockchain) < 1):
        return None
    return blockchain[-1]


def verify_transaction(transaction):
    sender_balance=get_balance(transaction['sender'])
    return sender_balance >= transaction['amount']



def add_transaction(recipient, sender=owner, amount=1.0):
    """Function to add the transaction value and also to 
    store the last transaction

    Args:
    sender: Sender of the coins.
    recipient: Recipient of the coins.
    amount: Amount of coins sent by the sender
    """
    
    transaction = {'sender': sender,
                   'recipient': recipient,
                   'amount': amount}
    
    if verify_transaction(transaction):
        open_transactions.append(transaction)
        save_data()
        participants.add(sender)
        participants.add(recipient)
        return True
    else:
        return False


def get_balance(participant):
    tx_sender = [
        [el['amount'] for el in block['transactions'] if el['sender'] == participant] 
        for block in blockchain
    ]
    open_tx_sender = [trans['amount'] for trans in open_transactions if trans["sender"] == participant]
    tx_sender.append(open_tx_sender)
    print(tx_sender)
    send_amount = functools.reduce(
        lambda tx_sum, tx_amt: tx_sum + (sum(tx_amt) if len(tx_amt) > 0 else 0),
        tx_sender,
        0
    )

    tx_receiver = [
        [el['amount'] for el in block['transactions'] if el['recipient'] == participant] 
        for block in blockchain
    ]

    received_amount = functools.reduce(
        lambda tx_sum, tx_amt: tx_sum + (sum(tx_amt) if len(tx_amt) > 0 else 0),
        tx_receiver,
        0
    )

    return received_amount - send_amount


def valid_proof(transactions,last_hash, proof):
    #Block hash
    guess=(str(transactions) + str(last_hash) +str(proof)).encode()
    guess_hash=hash_string_256(guess)
    print(guess_hash)
    return guess_hash[0:2] == '00'


def proof_of_work():
    last_block=blockchain[-1]
    last_hash=hash_block(last_block)
    proof=0
    while not valid_proof(open_transactions,last_hash,proof):
        proof +=1
    return proof


def mine_block():
    last_block=blockchain[-1]
    hashed_block= hash_block(last_block)
    proof=proof_of_work()
    # reward_transaction={
    #     'sender':"MINIG",
    #     'recipient':owner,
    #     'amount':MINING_REWARD,
    
    # }
    reward_transaction=OrderedDict([('sender','MINING'),('recipient',owner),('amount',MINING_REWARD)])
    copied_transaction=open_transactions[:]

    copied_transaction.append(reward_transaction)
    block={
        "previous_hash":hashed_block,
        "index":len(blockchain),
        "transactions":copied_transaction,
        'proof':proof,
    }
    #print(block)
    blockchain.append(block)
    save_data()
    return True

def get_transactional_value():
    """Taking the user input for the amount"""
    tx_recipient=input("Enter the recipient name:- ")
    tx_amount=float(input("Enter the amount:- "))
    return (tx_recipient,tx_amount)


def get_user_input():
    userInput=input("Your choice: ")
    return userInput


def print_blockchain():
    #Printing the blocks of the blockchain
    for block in blockchain:
        print("Outputting Block")
        print(block)


def verify_chain():
  for (index,data) in enumerate(blockchain):
      if(index == 0):
          continue
      elif(data["previous_hash"] != hash_block(blockchain[index-1])):
          return False
      if not valid_proof(data['transactions'][:-1],data["previous_hash"],data['proof']):
          print("Proof of work is invalid!")
          return False
  return True

def verify_transactions():
    return all([verify_transaction(tx) for tx in open_transactions])


waiting_for_input=True
while waiting_for_input:
    print("Please choose!")
    print("1. Enter a new transaction value")
    print("2. Display blockchain blocks")
    print("3. Mine a block")
    print("4. Output participants")
    print("5. Manipulate the blockchain")
    print("6. Verify Transaction")
    print("7. Quit")


    userInput=get_user_input()

    if(userInput == '1'):
        tx_data=get_transactional_value()
        recipient,amount=tx_data
        if add_transaction(recipient,amount=amount):
            print("Transaction Added!")
        else:
            print("Transaction Failed!")
        #print(open_transactions)
    elif(userInput == '2'):
        print_blockchain()
    elif(userInput=='3'):
      if  mine_block() is True:
          open_transactions=[]
    elif (userInput == '4'):
        print(participants)
    elif (userInput == '5'):
        if(len(blockchain) >=1):
            blockchain[0]={
            "previous_hash":"",
            "index":0,
            "transactions":[{'sender':"Taimoor Haider", "recipient":"Usama", 'amount':100.0}]
            }
    elif(userInput == '6'):
        if verify_transactions():
            print("All transactions are valid")
        else:
            print("Some transactions are invalid")
    elif(userInput == '7'):
       waiting_for_input=False    
    else:
        print("Input is invalid please select the right option!!!") 
    if not verify_chain():
        print_blockchain()
        print("Invlaid blockchain!!!")
        break 
    print("Balance of {}: {:6.2f}".format('Taimoor Haider',get_balance("Taimoor Haider")))
     

print("Done")