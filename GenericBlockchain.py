""" 
Imports ===============================================
    -> datetime: pegar data e hora atual para implementação nos blocos
    -> hashlib: usar, executar e/ou criar hashs, tais como hash256
    -> json: codificação dos blocos 
    -> flask and jsonify: Uso no postman, para vizualização de dados 
"""
import datetime
import hashlib
import json
from flask import Flask, jsonify 
"""====================================================="""


"""Class blockchain de uso generico"""
class Blockchain:
    
    #Criação do bloco genesis.
    def __init__(self):
        self.chain = [] 
        self.create_block(proof = 1, previous_hash = '0')
        
        
    #Criação de bloco adicionais genericos 
    def create_block(self, proof, previous_hash):
        block = {'index':len(self.chain)+1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof':proof,
                 'previus_hash':previous_hash}
        self.chain.append(block)
        return block
    
    
    #Pegar bloco anterior
    def get_previous_block(self):
        return self.chain[-1]
    
    
    #Nounce Teste (Mineração)
    def proof_of_work(self,previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof
    
    
    #validação do proof_of_work
    def hash(self,block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    
    #Validação do blockChain no todo
    def is_chain_valid(self,chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2-previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True

""" END CLASS ==================================================================="""

app = Flask(__name__)
blockchain = Blockchain()

@app.route('/mine_block', methods = ['GET'])

#Função de mineração
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.creat_block(proof, previous_hash)
    response = {'message': 'Parabens, vc minerou um bloco!',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash':block['previous_hash']}
    return jsonify(response)

#Função de mineração para pegar todo o blockchain
@app.route('/get_chain', methods = ['GET'])
def get_chain():
    response = {'chain':blockchain.chain,
                'length':len(blockchain.chain)}
    return jsonify(response),200


app.run(host='0.0.0.0', port=5000)

    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    