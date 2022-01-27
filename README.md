# Blockchain_Python
EM DESENVOLVIMENTO.

## Sobre:
Esse projeto tem como intuito desenvolver uma rede gerérica blockchain do zero utilizando a linguagem python e bibliotecas de apoio.

### Conteudos implementados:
    - Criação de uma rede Blockchain que contem: 
        -- Possibilidade de mineração e inserção de blocos na rede via REST 
        -- Protocolos de consenso: Usado para armozinar a rede permitindo assim que todos tenham a mesma versão do blockchain 
    - Criação de uma cripto moeda mineravel na rede 
    - Implementação dos contratos inteligentes 

## Instalação:
pip install requests==2.18.4 
pip install flask 

## Informações para Execução:
- Endereço flask local inicial: http://127.0.0.1:5000/
    -- Para cada exemplo criado, a URL deve ser no seguinte formato: http://127.0.0.1:5001/metodo_escolhido
    -- EX: Para solicitar o blockchain de determinado usuario, alteramos a porta dele, e chamamos o metodo get_chain -> http://127.0.0.1:5003/get_chain 
- Cada vertente da run_coin.py deve ser executada simultaneamente para a geração dos dados transações
- Para verificar, solicitar e alterar dados, basta usar a aplicação PostMan (Software gratuito)


