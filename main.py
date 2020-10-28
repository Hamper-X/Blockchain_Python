# IMPORTS |=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
from blockchain import *
import datetime     #pegar data e hora exata
import hashlib      #criar e usar hashs especificas
import json         #produzir e ler dados e json

# MAIN |=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=

blockchain = Blockchain()

# FUNCTIONS |=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=

"""
    @ Função: Mineração do bloco  
    @ Parametros:   --//--
    @ Return: 
"""
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previus_hash = blockchain.hash(previous_block)
    block = blockchain.creat_block(proof,previus_hash)
    resp = {'message': 'Bloco Minerado',
            'index': block['index'],
            'timestamp':block['timestamp'],
            'proof':block['proof'],
            'previous_hash':block['previous_hash']}
    return jsonify(resp)