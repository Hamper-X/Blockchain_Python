# IMPORTS |=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
import datetime     #pegar data e hora exata
import hashlib      #criar e usar hashs especificas
import json
from operator import is_
from urllib import response         #produzir e ler dados e json
from flask import Flask, jsonify, request
from markupsafe import re
from numpy import block
from pandas import to_datetime
import requests
from uuid import uuid4  # Permite a geração de um endereço unico de um objeto 
from urllib.parse import urlparse



# CLASSE BLOCKCHAIN Convertida para MOEDA CRIPTOGRAFICA |=-=-=-=-=-=-=

class Blockchain:

    # Construtor 
    def __init__(self):
        self.chain = []
        self.transactions = []      # Transações
        self.create_block(proof = 1, previous_hash = '0')
        self.nodes = set() # Conjunto que obtem todos os nós participantes da rede

    """
        @ Funcao: criar novo bloco na chain 
        @ Parametros:
            - self (mostrando que é um metodo da classe)
            - proof (valor que a função de mineração passara)
            - previus_hash (conexão com o bloco anterior)
        @ Observacoes: possui suporte para transacoes 
    """
    def create_block(self, proof, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': str(datetime.datetime.now()),
            'proof': proof,
            'previous_hash': previous_hash,
            'transactions':self.transactions
        }
        self.transactions = []  # Quando o bloco é criado a lista de transações precisa ser zerada 
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
        @ Funcao: Adicionar transacao  
        @ Parametros:
            - self      (mostrando que é um metodo da classe)
            - sender    (quem enviou)
            - receiver  (quem recebeu)
            - amount    (valor/quantidade)
        @ Return: index do bloco em que a transacao foi adicionada
    """
    def add_transaction(self,sender,receiver, amount):
        self.transactions.append({
            'sender':sender,
            'receiver':receiver,
            'amount':amount
        })
        previous_block = self.get_previous_block()
        return previous_block['index'] + 1

    """
        @ Função: Adição de nós via endereço conforme é recebido 
        @ Parametros:
            - self (mostrando que é um metodo da classe)
            - address (endereço)
        @ Obs: Endereco padrao do flask: 'http://127.0.0.1:5000/'
    """
    def add_node(self,address):
        parsed_url = urlparse(address)
        # Netloc captura somente o endereco que queremos ( http://127.0.0.1:5000/ ==> 127.0.0.1:5000)
        self.nodes.add(parsed_url.netloc)   # Adicionando esse endereço a lista(ao conjunto de nós)

    """
        @ Função: substituição da cadeia caso ela encontre uma cadeia que seja maior (protocolo de consenso) 
        @ Parametros:
            - self (mostrando que é um metodo da classe)
    """  
    def replace_chain(self):
        network = self.nodes            # Copia dos nós
        longest_chain = None            # boolean - verificação para maior cadeia
        max_length = len(self.chain)    # Pegando comprimento maximo do blockchain
        
        # Percorrendo cada nó da rede 
        for node in network:
            response = requests.get(f'http://{node}/get_chain') # Envio via REST passando o o servico get_chain e a porta {node}
            if response.status_code == 200:     # Verificação de validação de requisição (codigo 200 validado)
                length = response.json()['length']  # Pagina retorna todo o comprimento, por isso guardaremos apenas o tamanho do blockchain retornado
                chain = response.json()['chain']
                if length > max_length and self.is_chain_valid(chain):
                    max_length = length     # Atualização do maior tamanho
                    longest_chain = chain   # Atualização do chain mais longo

        if longest_chain:
            self.chain = longest_chain  # Atualização o self.chain
            return True
        return False


# MAIN /=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=
app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False   # Comando necessario para aplicação do Flask nas novas versões
node_address = str(uuid4()).replace('-','')     #Transformando o endereço em texto e retirando os traços contidos entre os valores
blockchain = Blockchain()


"""
    @ Função: mineração do bloco 
    @ Parametros:Objeto blockchain
    @ Return: json formatado com o bloco minerado e codigo de resposta
"""
@app.route('/mine_block', methods = ['GET'])    # GET: Serve apenas para pegar. não envia dados e nem cria.
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    blockchain.add_transaction(sender= node_address,receiver="Lucas",amount=10)     # Adicionando a transação ao blockchain
    block = blockchain.create_block(proof, previous_hash)
    response = {'message': 'Parabens voce acabou de minerar um bloco!',
                'index':            block['index'],
                'timestamp':        block['timestamp'],
                'proof':            block['proof'],
                'previous_hash':    block['previous_hash'],
                'transaction':      block['transactions']}
    return jsonify(response), 200  

"""
    @ Função: Mostrar toda rede blockchain  
    @ Parametros:
        - Objeto blockchain
    @ Return: json formatado com o bloco minerado
"""
@app.route('/get_chain', methods = ['GET'])
def get_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200

"""
    @ Função: validar toda rede blockchain  
    @ Parametros:
        - Objeto blockchain
    @ Return: json formatado com a mensagem de validação
"""
@app.route('/is_valid', methods = ['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {'message' : ' Blockchain validado! '}
    else:
        response = {'message' : ' ERRO! Blockchain não valido. '}
    return jsonify(response), 200

"""
    @ Função: Adicao de transacao 
    @ Return: json com codigo de validacao da operacao
"""
@app.route('/add_transaction', methods = ['POST'])  # Usamos post pq estamos criamos algo, no caso uma transação.
def add_transaction():
    json = request.get_json()   # Pegar o arquivo json que o postman vai enviar e salva-lo na variavel json
    transaction_key = ['sender','receiver','amont'] # Verificando se a transação é valida verificando as chaves
    if not all(key in json for key in transaction_key):
        return 'ERRO! A transação possui elementos em falta. Servidor não pode concluir a solicitação.', 400
    
    index = blockchain.add_transaction(json['sender'],json['receiver'],json['amount'])
    response = {'messege':f'Esta transacao sera adicionada ao bloco {index}'}
    return jsonify(response), 201 # Codigo 201 utilizado para quando temos um post com sucesso

"""
    @ Função: Request com retorno de todos os nos da rede 
    @ Return: json formatado com todos os nós da rede 
"""
@app.route('/connect_node', methods = ['POST'])
def connect_node():
    json = request.get_json()
    nodes = json.get('nodes')

    # Verificar se a requisicao nao esta vazia 
    if nodes is None:
        return "ERRO! Conexão do nó foi invalida.", 400
    for node in nodes:
        blockchain.add_node(node)
    response = {'message':'Todos os nós foram contabilizados e aderidos a rede:', 'total_nodes':list(blockchain.nodes)}
    return jsonify(response),201

"""
    @ Função: Request para substituir a chain local
    @ Return: 
"""
@app.route('/replace_chain',methods = ['GET'])
def replace_chain():
    is_chain_replaced = blockchain.replace_chain()
    if is_chain_replaced:
        response = {'message':'ALERTA! Detectado blockchain local alterado ou desatualizado. Atualizando blockchain.',
        'new_chain': blockchain.chain}
    else:
        response = {'message':'ALERTA! Verificação da blockchain concluida. Nenhum processo ou alteração pendente.',
        'actual_chain':blockchain.chain}
    
    return jsonify(response),201



app.run(host = '0.0.0.0', port = 5000) # Porta 5000 será a porta inicial (Para cada no será agregado uma nova porta)

