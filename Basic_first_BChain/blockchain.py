import datetime
import hashlib
import json

from flask import Flask, jsonify


class MyBlockChain:

    def __init__(self):
        self.chain = []
        self.create_new_block(proof=1, previous_hash='0')

    def create_new_block(self, proof, previous_hash):
        block = {'index': len(self.chain) + 1, 
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash}

        self.chain.append(block)
        return block

    def fetch_last_block_in_chain(self):
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        naunce = 1
        check_proof = False
        while check_proof is False:
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

app = Flask(__name__)


blockchain = MyBlockChain()

@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = blockchain.fetch_last_block_in_chain()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_new_block(proof, previous_hash)
    response = {'message': 'Congrats! Block was mined and added to blockchain',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof':  block['proof'],
                'previous_hash': block['previous_hash']}
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

app.run(host = '0.0.0.0', port=5000)