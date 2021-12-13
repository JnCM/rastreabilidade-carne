from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import json
from site_app.dao import models
from site_app.utils import utils
from django.db.models import Max
from rastreio_carne_ufv import blockchain_connect, settings
import hashlib
from django.forms.models import model_to_dict
import asyncio

def cadastro_fazenda(request):
    if request.user.is_authenticated:
        return render(request, 'cadastro_fazenda.html', {"logado": 1})
    return HttpResponseRedirect("/login")


async def salvar_fazenda(request):
    if request.method == "POST":
        nomeFazenda = request.POST.get("nome_fazenda")
        localizacaoFazenda = request.POST.get("localizacao_fazenda")
        tipoCriacao = request.POST.get("tipo_criacao")
        idFazenda = proximoIdFazenda()
        if not verificaFazenda(nomeFazenda):
            msg = "FAZENDA EXISTENTE"
        else:
            novaFazenda = models.Fazenda(
                id_fazenda=idFazenda,
                nome_fazenda=nomeFazenda,
                localizacao_fazenda=localizacaoFazenda,
                tipo_criacao=tipoCriacao
            )
            json_gen_hash = model_to_dict(novaFazenda)
            valor_hash = hashlib.md5(str(json_gen_hash).encode())
            loop = asyncio.get_event_loop()
            id_blockchain = loop.run_until_complete(blockchain_connect.setDado(settings.CONTRACT, settings.W3_CONNECTION, valor_hash.hexdigest()))
            if id_blockchain != -1:
                id_hash = utils.proxIdHash()
                novoItem = models.Hash(
                    id_hash=id_hash,
                    id_tabela=1,
                    id_item=str(idFazenda),
                    id_hash_blockchain=id_blockchain
                )
                novoItem.save(force_insert=True)
                novaFazenda.save(force_insert=True)
                msg = "OK"
            else:
                msg = "ERRO"
    return HttpResponse(json.dumps({'resposta': msg}))


def proximoIdFazenda():
    fazendas = models.Fazenda.objects.all()
    if len(fazendas) == 0:
        return 1

    proximoId = int(fazendas.aggregate(Max('id_fazenda'))["id_fazenda__max"]) + 1
    return proximoId

def verificaFazenda(nome):
    retorno = models.Fazenda.objects.filter(nome_fazenda=nome)
    if len(retorno) > 0:
        return False
    return True
