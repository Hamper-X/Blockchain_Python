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
        self.chain.append(block)                            # .append para adionar o bloco
        return block