from celery import shared_task
from . import settings
from site_app.utils import utils

@shared_task
def setDado(dado, json_dado, tabela):
    try:
        trans = settings.CONTRACT.functions.addInfo(dado).buildTransaction({'nonce': returnNonceDado(),'from': settings.BLOCKCHAIN_ACCOUNT})
        signed_txn = settings.W3_CONNECTION.eth.account.sign_transaction(trans, private_key=settings.PK_ACCOUNT)
        tx_hash = settings.W3_CONNECTION.eth.sendRawTransaction(signed_txn.rawTransaction)
        settings.W3_CONNECTION.eth.waitForTransactionReceipt(tx_hash) # caso precise aguardar o término da transação na blockchain
        id_blockchain = int(settings.W3_CONNECTION.eth.getTransactionReceipt(tx_hash)['logs'][0]['data'],16)
        msg = utils.salvar_dado_banco(id_blockchain, json_dado, tabela)
        #print("Codigo registrado: ", id_blockchain)
        return msg
    except Exception as error:
        print(error)
        return "ERRO_BLOCKCHAIN"

def getDado(id_dado):
    try:
        retorno = settings.CONTRACT.functions.seeInfo(id_dado).call({'from': settings.BLOCKCHAIN_ACCOUNT})
        #print(retorno)
        return retorno
    except Exception as error:
        print(error)
        return -1

def returnNonceDado():
    totalTransactions = settings.W3_CONNECTION.eth.getTransactionCount(settings.BLOCKCHAIN_ACCOUNT, 'pending')
    return totalTransactions
