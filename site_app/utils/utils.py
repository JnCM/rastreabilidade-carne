import json
from site_app.dao import models
from django.db.models import Max
import qrcode, io

def proxIdHash():
    hashes = models.Hash.objects.all()
    if len(hashes) == 0:
        return 1

    proximoId = int(hashes.aggregate(Max('id_hash'))["id_hash__max"]) + 1
    return proximoId


def salvar_dado_banco(id_blockchain, json_dado, tabela):
    try:
        if tabela == 1: # Fazenda
            id_hash = proxIdHash()
            novoItem = models.Hash(
                id_hash=id_hash,
                id_tabela=1,
                id_item=str(json_dado["id_fazenda"]),
                id_hash_blockchain=id_blockchain
            )
            novoItem.save(force_insert=True)
            novaFazenda = models.Fazenda(**json_dado)
            novaFazenda.save(force_insert=True)
        elif tabela == 2: # Animal
            id_hash = proxIdHash()
            novoItem = models.Hash(
                id_hash=id_hash,
                id_tabela=2,
                id_item=json_dado["id_animal"],
                id_hash_blockchain=id_blockchain
            )
            novoItem.save(force_insert=True)
            novoAnimal = models.Animal(**json_dado)
            novoAnimal.save(force_insert=True)
        elif tabela == 3: # Vacina
            id_hash = proxIdHash()
            novoItem = models.Hash(
                id_hash=id_hash,
                id_tabela=3,
                id_item=str(json_dado["id_vacina"]),
                id_hash_blockchain=id_blockchain
            )
            novoItem.save(force_insert=True)
            novaVacina = models.Vacina(**json_dado)
            novaVacina.save(force_insert=True)
        elif tabela == 4: # Terminação
            id_hash = proxIdHash()
            novoItem = models.Hash(
                id_hash=id_hash,
                id_tabela=4,
                id_item=str(json_dado["id_terminacao"]),
                id_hash_blockchain=id_blockchain
            )
            novoItem.save(force_insert=True)
            novaTerminacao = models.Terminacao(**json_dado)
            novaTerminacao.save(force_insert=True)
        elif tabela == 5: # Venda
            id_hash = proxIdHash()
            novoItem = models.Hash(
                id_hash=id_hash,
                id_tabela=5,
                id_item=str(json_dado["id_venda"]),
                id_hash_blockchain=id_blockchain
            )
            novoItem.save(force_insert=True)
            novaVenda = models.Venda(**json_dado)
            novaVenda.save(force_insert=True)
        elif tabela == 6: # Item da venda
            id_hash = proxIdHash()
            novoItem = models.Hash(
                id_hash=id_hash,
                id_tabela=6,
                id_item=str(json_dado["id_item"]),
                id_hash_blockchain=id_blockchain
            )
            novoItem.save(force_insert=True)
            novoItemVenda = models.VendaAnimal(**json_dado)
            novoItemVenda.save(force_insert=True)
        elif tabela == 7: # Frigorífico
            id_hash = proxIdHash()
            novoItem = models.Hash(
                id_hash=id_hash,
                id_tabela=7,
                id_item=str(json_dado["id_frigorifico"]),
                id_hash_blockchain=id_blockchain
            )
            novoItem.save(force_insert=True)
            novoFrigorifico = models.Frigorifico(**json_dado)
            novoFrigorifico.save(force_insert=True)
        elif tabela == 8: # Abate
            id_hash = proxIdHash()
            novoItem = models.Hash(
                id_hash=id_hash,
                id_tabela=8,
                id_item=str(json_dado["id_abate"]),
                id_hash_blockchain=id_blockchain
            )
            novoItem.save(force_insert=True)
            novoAbate = models.Abate(**json_dado)
            novoAbate.save(force_insert=True)
        elif tabela == 9: # Qualidade
            id_hash = proxIdHash()
            novoItem = models.Hash(
                id_hash=id_hash,
                id_tabela=9,
                id_item=str(json_dado["id_qualidade"]),
                id_hash_blockchain=id_blockchain
            )
            novoItem.save(force_insert=True)
            novaQualidade = models.Qualidade(**json_dado)
            novaQualidade.save(force_insert=True)
        elif tabela == 10: # Embalagem
            id_hash = proxIdHash()
            novoItem = models.Hash(
                id_hash=id_hash,
                id_tabela=10,
                id_item=str(json_dado["id_embalagem"]),
                id_hash_blockchain=id_blockchain
            )
            novoItem.save(force_insert=True)
            novaEmbalagem = models.Embalagem(**json_dado)
            novaEmbalagem.save(force_insert=True)
            img = qrcode.make('https://rastreio-carne.herokuapp.com/embalagens/{}'.format(json_dado["id_embalagem"]))
            img_bytes = io.BytesIO()
            img.save(img_bytes, format="PNG")
            img_bytes = img_bytes.getvalue()
            if json_dado['tipo_corte'] == "PC":
                tipoCorte = "picanha"
            elif json_dado['tipo_corte'] == "FR":
                tipoCorte = "fraldinha"
            elif json_dado['tipo_corte'] == "FM":
                tipoCorte = "filemignon"
            else:
                tipoCorte = "contrafile"
            nome_imagem = "{}_{}_{}.png".format(tipoCorte, json_dado["id_embalagem"], json_dado['peso_corte'])
            idQrcode = proximoIdQrcode()
            novoQrcode = models.Qrcode(
                id_qrcode=idQrcode,
                nome_imagem=nome_imagem,
                binario_imagem=img_bytes,
                id_embalagem=json_dado["id_embalagem"]
            )
            novoQrcode.save(force_insert=True)
        elif tabela == 11: # Comercialização
            id_hash = proxIdHash()
            novoItem = models.Hash(
                id_hash=id_hash,
                id_tabela=11,
                id_item=str(json_dado["id_comercializacao"]),
                id_hash_blockchain=id_blockchain
            )
            novoItem.save(force_insert=True)
            novaComercializacao = models.Comercializacao(**json_dado)
            novaComercializacao.save(force_insert=True)
        elif tabela == 12: # Item da comercialização (embalagem vendida)
            id_hash = proxIdHash()
            novoItem = models.Hash(
                id_hash=id_hash,
                id_tabela=12,
                id_item=str(json_dado["id_item"]),
                id_hash_blockchain=id_blockchain
            )
            novoItem.save(force_insert=True)
            novaComercializacaoEmbalagem = models.ComercializacaoEmbalagem(**json_dado)
            novaComercializacaoEmbalagem.save(force_insert=True)
        return "OK"
    except Exception as e:
        print(e)
        return "ERRO_DADOS"


def proximoIdQrcode():
    qrcodes = models.Qrcode.objects.all()
    if len(qrcodes) == 0:
        return 1

    proximoId = int(qrcodes.aggregate(Max('id_qrcode'))["id_qrcode__max"]) + 1
    return proximoId