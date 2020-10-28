# IMPORTS |=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

import datetime     #pegar data e hora exata
import hashlib      #criar e usar hashs especificas
import json         #produzir e ler dados e json

# CLASSE BLOCKCHAIN |=-=-=-=-=-=-=-=-=-=-=-

class Blockchain:
    def __init__(self):
        self.chain = [] #lista chain
        self.creat_block(proof =1, previous_hash = '0')
    

    """
        @ Função: criar novo bloco na chain 
        @ Parametros:
            - self (mostrando que é um metodo da classe)
            - proof (valor que a função de mineração passara)
            - previus_hash (conexão com o bloco anterior)
    """    
    def creat_block(self,proof,previus_hash):
        block = {'index':len(self.chain)+ 1,                # Indice do bloco 
                'timestamp':str(datetime.datetime.now()),   # Hora de criação
                'proof' : proof,                            # Hash valido 
                'previus_hash':previus_hash}                # Link bloco anterior
        self.chain.append(block)                            # .append para adicionar o bloco
        return block
    
    """
        @ Função: Pegar bloco anterior
        @ Parametros: Self
        @ Retorno: bloco anterior
    """
    def get_previous_block(self):
        return self.chain[-1]                # Retorno do bloco anterior

    """
        @ Função: criação de prova de trabalho 
        @ Parametros:
            - self (mostrando que é um metodo da classe)
            - previus_proof (proof do bloco anterior a ser validado)
        @ Return: new_proof (novo proof do bloco aceito)
    """
    def proof_of_work (self,previous_proof):
        new_proof = 1
        check_proof = False                 # Variavel para checagem da operação
        while check_proof is False:
            # Nivel de dificuldade: 4 '0' a esquerda (quanto mais zeros, mais dificil)
            hash_operation = hashlib.sha256(str(new_proof**2-previous_proof**2).encode()).hexdigest()       # Geração da hash com a biblioteca hashlib
            if hash_operation[:4] == '0000':    # Se tiver 4 '0' a esquerda, o hash_operation sera validado
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
        encoded_block = json.dumps(block, sort_keys=True).encode()   # Gerar um json ordenado pela chave com base no dicionario block
        return hashlib.sha256(encoded_block).hexdigest()
    
    """
        @ Função: Validação do blockchain  
        @ Parametros:
            - self (mostrando que é um metodo da classe)
            - chain (lista de blocos do blockchain)
        @ Return: validado ou nao (booleano)
    """
    def is_chain_valid(self,chain):
        previous_block = chain[0]       # Incio no primeiro bloco
        block_index = 1                 # Localização de bloco
        while block_index < len(chain): # Loop para testar toda rede
            block = chain[block_index]  
            if block['previous_hash'] != self.hash(previous_block): # Primeira validação: Hash do bloco anterior com o atual
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':    # Verificação do nivel de dificuldade (4 zeros a esquerda)
                return False
            previous_block = block
            block_index += 1
            return True

    """
        @ Função: Mineração do bloco  
        @ Parametros:   --//--
        @ Return: 
    """
    def mine_block(self):
        previous_block = get_previous_block()
        previous_proof = previous_block['proof']
        proof = proof_of_work(previous_proof)
        previus_hash = hash(previous_block)
