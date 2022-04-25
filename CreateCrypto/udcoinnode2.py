from crypt import methods
import datetime
import hashlib
import json
from urllib import response
import requests
from uuid import uuid4
from flask import Flask, jsonify, request
from urllib.parse import urlparse


class MyBlockChain:

    def __init__(self):
        self.chain = []
        self.transactions = []
        self.create_new_block(proof=1, previous_hash='0')
        self.nodes = set()

    def create_new_block(self, proof, previous_hash):
        block = {'index': len(self.chain) + 1, 
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash,
                 'transactions' : self.transactions}
        self.transactions = []
        self.chain.append(block)
        return block

    def fetch_last_block_in_chain(self):
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        naunce = 1
        check_proof = False
        while not check_proof:
            hash_operation = hashlib.sha256(str(naunce**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                naunce += 1
        return naunce

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_position = 1
        while block_position < len(chain):
            block = chain[block_position]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_position += 1
        return True

    def add_transactions(self, sender, reciever, amount):
        self.transactions.append({'sender' : sender, 'reciever': reciever, 'amount': amount})
        previous_block = self.fetch_last_block_in_chain()
        return previous_block['index'] + 1

    def add_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def replace_chain(self):
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)
        for nodes in network:
            response = requests.get(f'http://{nodes}/get_full_chain')
            if response.status_code == 200:
                length = response.json()['length_of_chain']
                chain = response.json()['chain']
                if length > max_length and self.is_chain_valid(chain):
                    max_length = length
                    longest_chain = chain
        if longest_chain:
            self.chain = longest_chain
            return True
        return False


app = Flask(__name__)

#address of node
node_address = str(uuid4()).replace('-', '')


blockchain = MyBlockChain()

@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = blockchain.fetch_last_block_in_chain()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    blockchain.add_transactions(sender=node_address, reciever='node2', amount = 20)
    block = blockchain.create_new_block(proof, previous_hash)
    response = {'message': 'Congrats! Block was mined and added to blockchain',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof':  block['proof'],
                'previous_hash': block['previous_hash'],
                'transactions': block['transactions']}
    return jsonify(response), 200

@app.route('/get_full_chain', methods=['GET'])
def get_chain():
    response = {'chain': blockchain.chain,
                'length_of_chain': len(blockchain.chain)}
    return jsonify(response), 200

@app.route('/is_chain_valid', methods=['GET'])
def check_chain():
    response = {'chain_valid': blockchain.is_chain_valid(blockchain.chain)}
    return jsonify(response), 200

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    json = request.get_json()
    transaction_keys = ['sender', 'receiver', 'amount']
    if not all (key in json for key in transaction_keys):
        return 'Some elements are missing in transaction', 400
    index = blockchain.add_transactions(json['sender'], json['receiver'], json['amount'])
    response = {'message' : f'Transaction will be added to block index {index}'}
    return jsonify(response), 201

@app.route('/connect_node', methods=['POST'])
def connect_node():
    json = request.get_json()
    nodes = json.get('nodes')
    if nodes is None or len(nodes) < 1:
        return "No Nodes passed in request", 400
    for node in nodes:
        blockchain.add_node(node)
    response = {'message': 'all the nodes are now connected. The UDCOIN blockchain now containes following nodes',
                'total_nodes': list(blockchain.nodes)}
    return jsonify(response), 201

@app.route('/replace_chain', methods=['GET'])
def replace_chain():
    is_chain_replaced = blockchain.replace_chain()
    if is_chain_replaced:
        response = {'message' : 'The node had different chain, hence replaced with longest chain',
                     'new_chain' : blockchain.chain}
    else:
        response = {'message' : 'Your chain is longest chain. ',
                    'actual_chain' : blockchain.chain}
    return jsonify(response), 200



app.run(host = '0.0.0.0', port=5002)