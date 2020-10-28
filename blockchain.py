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
        @ Função: verificação de prova de trabalho 
        @ Parametros:
            - self (mostrando que é um metodo da classe)
            - previus_proof (proof do bloco anterior a ser validado)
        @ Return: 
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
