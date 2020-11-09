# IMPORTS |=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

import datetime     #pegar data e hora exata
import hashlib      #criar e usar hashs especificas
import json         #produzir e ler dados e json

# CLASSE BLOCKCHAIN |=-=-=-=-=-=-=-=-=-=-=-
class Blockchain:

    def __init__(self):
        self.chain = []
        self.create_block(proof = 1, previous_hash = '0')


    """
        @ Função: criar novo bloco na chain 
        @ Parametros:
            - self (mostrando que é um metodo da classe)
            - proof (valor que a função de mineração passara)
            - previus_hash (conexão com o bloco anterior)
    """
    def create_block(self, proof, previous_hash):
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash}
        self.chain.append(block)
        return block

    """
        @ Função: Pegar bloco anterior
        @ Parametros: Self
        @ Retorno: bloco anterior
    """
    def get_previous_block(self):
        return self.chain[-1]

    """
        @ Função: criação de prova de trabalho 
        @ Parametros:
            - self (mostrando que é um metodo da classe)
            - previus_proof (proof do bloco anterior a ser validado)
        @ Return: new_proof (novo proof do bloco aceito)
    """
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
                print("nao deu certo ",new_proof)
        return new_proof
    
    """
        @ Função: Pegar o bloco e transforma em json, encriptografando-o com hash256  
        @ Parametros:
            - self (mostrando que é um metodo da classe)
            - bloco (lista self.chain da classe)
        @ Return: json encriptografado
    """
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    """
        @ Função: Validação do blockchain  
        @ Parametros:
            - self (mostrando que é um metodo da classe)
            - chain (lista de blocos do blockchain)
        @ Return: validado ou nao (booleano)
    """
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True

"""
    @ Função: mineração do bloco
    @ Parametros:
        - Objeto blockchain
    @ Return: json formatado com o bloco minerado
"""
def mine_block(blockchain):
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    response = {'message': 'Bloco minerado com sucesso!',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash']}
    json_object = json.dumps(response, indent = 4)   
    return json_object

"""
    @ Função: Mostrar toda rede blockchain  
    @ Parametros:
        - Objeto blockchain
    @ Return: json formatado com o bloco minerado
"""
def get_chain(blockchain):
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    json_object = json.dumps(response, indent = 4)   
    return json_object

"""
    @ Função: validar toda rede blockchain  
    @ Parametros:
        - Objeto blockchain
    @ Return: json formatado com a mensagem de validação
"""
def is_valid(blockchain):
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {'message' : ' BLockchain validado! '}
    else:
        response = {'message' : ' ALERT! Blockchain não valido. '}
    json_object = json.dumps(response, indent = 4)   
    return json_object

# MAIN /=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=
blockchain = Blockchain()
while True:
    print("=-=-=-=-=-=-=-=-=-=-=-=|| MENU ||=-=-=-=-=-=-=-=-=-=-=-=")
    print("""[1] Minerar Bloco      [2] Verificar rede      [3] Mostrar rede      [4] Sair""")
    resp = int(input())
    if resp == 1:
        print(mine_block(blockchain))
    elif resp == 2:
        print(is_valid(blockchain))
    elif resp == 3:
        print(get_chain(blockchain))
    else:
        break
        


