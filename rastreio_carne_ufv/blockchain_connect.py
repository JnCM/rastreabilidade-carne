import json, os
from web3 import Web3
from environs import Env

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

env = Env()
env.read_env(os.path.join(BASE_DIR, '.env'), recurse=False)

PROVIDER = env.str("PROVIDER")
BLOCKCHAIN_ACCOUNT = env.str("BLOCKCHAIN_ACCOUNT")
PK_ACCOUNT = env.str("PK_ACCOUNT")
CONTRACT_ABI = env.str("CONTRACT_ABI")
HASH_CONTRACT = env.str("HASH_CONTRACT")

def conectarContrato():
    try:
        #Conexão com provider
        web3 = Web3(Web3.HTTPProvider(PROVIDER))
        if not(web3.isConnected()):
            print("Erro de conexão")
            return None, None
        
        #Dados do contrato storage.sol     
        abi = json.loads(CONTRACT_ABI)
        tx_hash = HASH_CONTRACT
        tx_receipt = web3.eth.getTransactionReceipt(tx_hash)
        contratoDados = web3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
        #print("Conectado!")
        return web3, contratoDados
    except:
        print("Erro interno")
        return None, None
        
def setDado(contrato, w3_con, dado):
    try:
        trans = contrato.functions.addInfo(dado).buildTransaction({'nonce': returnNonceDado(w3_con),'from': BLOCKCHAIN_ACCOUNT})
        signed_txn = w3_con.eth.account.sign_transaction(trans, private_key=PK_ACCOUNT)
        tx_hash = w3_con.eth.sendRawTransaction(signed_txn.rawTransaction)
        w3_con.eth.waitForTransactionReceipt(tx_hash) # caso precise aguardar o término da transação na blockchain
        id_blockchain = int(w3_con.eth.getTransactionReceipt(tx_hash)['logs'][0]['data'],16)
        #print("Codigo registrado: ", id_blockchain)
        return id_blockchain
    except Exception as error:
        print(error)
        return -1

def getDado(contrato, id_dado):
    try:
        retorno = contrato.functions.seeInfo(id_dado).call({'from': BLOCKCHAIN_ACCOUNT})
        #print(retorno)
        return retorno
    except Exception as error:
        print(error)
        return -1

def returnNonceDado(w3_con):
    totalTransactions = w3_con.eth.getTransactionCount(BLOCKCHAIN_ACCOUNT, 'pending')
    return totalTransactions
