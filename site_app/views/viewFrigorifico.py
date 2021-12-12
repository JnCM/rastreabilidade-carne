from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import json
from site_app.dao import models
from site_app.utils import utils
from django.db.models import Max
from rastreio_carne_ufv import blockchain_connect, settings
import hashlib
from django.forms.models import model_to_dict

def cadastro_frigorifico(request):
    if request.user.is_authenticated:
        return render(request, 'cadastro_frigorifico.html', {"logado": 1})
    return HttpResponseRedirect("/login")


def salvar_frigorifico(request):
    if request.method == "POST":
        nomeFrigorifico = request.POST.get("nome_frigorifico")
        localizacaoFrigorifico = request.POST.get("localizacao_frigorifico")
        cnpj = request.POST.get("cnpj").replace(".", "").replace("/", "").replace("-", "")
        responsavel = request.POST.get("responsavel")
        idFrigorifico = proximoIdFrigorifico()
        if not verificaFrigorifico(cnpj):
            msg = "FRIGORIFICO EXISTENTE"
        else:
            novoFrigorifico = models.Frigorifico(
                id_frigorifico=idFrigorifico,
                nome_frigorifico=nomeFrigorifico,
                localizacao_frigorifico=localizacaoFrigorifico,
                cnpj=cnpj,
                responsavel=responsavel
            )
            json_gen_hash = model_to_dict(novoFrigorifico)
            valor_hash = hashlib.md5(str(json_gen_hash).encode())
            id_blockchain = blockchain_connect.setDado(settings.CONTRACT, settings.W3_CONNECTION, valor_hash.hexdigest())
            if id_blockchain != -1:
                id_hash = utils.proxIdHash()
                novoItem = models.Hash(
                    id_hash=id_hash,
                    id_tabela=7,
                    id_item=str(idFrigorifico),
                    id_hash_blockchain=id_blockchain
                )
                novoItem.save(force_insert=True)
                novoFrigorifico.save(force_insert=True)
                msg = "OK"
            else:
                msg = "ERRO"
    return HttpResponse(json.dumps({'resposta': msg}))


def proximoIdFrigorifico():
    frigorificos = models.Frigorifico.objects.all()
    if len(frigorificos) == 0:
        return 1

    proximoId = int(frigorificos.aggregate(Max('id_frigorifico'))["id_frigorifico__max"]) + 1
    return proximoId

def verificaFrigorifico(cnpj):
    retorno = models.Frigorifico.objects.filter(cnpj=cnpj)
    if len(retorno) > 0:
        return False
    return True