from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import json
from site_app.dao import models
from site_app.utils import utils
from django.db.models import Max
from rastreio_carne_ufv import blockchain_connect, settings
import hashlib
from django.forms.models import model_to_dict


def cadastro_qualidade(request):
    if request.user.is_authenticated:
        animais = list(models.Animal.objects.all().values())
        for animal in animais:
            animal["data_nascimento"] = animal["data_nascimento"].strftime("%Y-%m-%d")
            hash_tb = list(models.Hash.objects.filter(id_tabela=2, id_item=str(animal['id_animal'])).values('id_hash_blockchain'))
            id_hash = hash_tb[0]['id_hash_blockchain']
            dado_hash = blockchain_connect.getDado(settings.CONTRACT, id_hash)
            hash_animal = hashlib.md5(str(animal).encode()).hexdigest()
            if hash_animal == dado_hash:
                animal['check_blockchain'] = True
            else:
                animal['check_blockchain'] = False
        return render(request, 'cadastro_qualidade.html', {'animais': animais, "logado": 1})
    return HttpResponseRedirect("/login")


def salvar_qualidade(request):
    if request.method == "POST":
        idAnimal = request.POST.get("animal")
        comprimentoSar = float(request.POST.get("comprimento_sarcomero"))
        forcaCis = float(request.POST.get("forca_cisalhamento"))
        perdaDesCong = float(request.POST.get("perda_descongelamento"))
        perdaCoccao = float(request.POST.get("perda_coccao"))
        corCarneL = request.POST.get("cor_carne_l")
        corCarneA = request.POST.get("cor_carne_a")
        corCarneB = request.POST.get("cor_carne_b")
        corGorduraL = request.POST.get("cor_gordura_l")
        corGorduraA = request.POST.get("cor_gordura_a")
        corGorduraB = request.POST.get("cor_gordura_b")
        idQualidade = proximoIdQualidade()
        if not verificaQualidade(idAnimal):
            msg = "QUALIDADE EXISTENTE"
        else:
            novaQualidade = models.Qualidade(
                id_qualidade=idQualidade,
                comprimento_sarcomero=comprimentoSar,
                forca_cisalhamento=forcaCis,
                perda_descongelamento=perdaDesCong,
                perda_coccao=perdaCoccao,
                cor_carne_l=corCarneL,
                cor_carne_a=corCarneA,
                cor_carne_b=corCarneB,
                cor_gordura_l=corGorduraL,
                cor_gordura_a=corGorduraA,
                cor_gordura_b=corGorduraB,
                id_animal=idAnimal
            )
            json_gen_hash = model_to_dict(novaQualidade)
            valor_hash = hashlib.md5(str(json_gen_hash).encode())
            id_blockchain = blockchain_connect.setDado(settings.CONTRACT, settings.W3_CONNECTION, valor_hash.hexdigest())
            if id_blockchain != -1:
                id_hash = utils.proxIdHash()
                novoItem = models.Hash(
                    id_hash=id_hash,
                    id_tabela=9,
                    id_item=str(idQualidade),
                    id_hash_blockchain=id_blockchain
                )
                novoItem.save(force_insert=True)
                novaQualidade.save(force_insert=True)
                msg = "OK"
            else:
                msg = "ERRO"
    return HttpResponse(json.dumps({'resposta': msg}))


def proximoIdQualidade():
    qualidades = models.Qualidade.objects.all()
    if len(qualidades) == 0:
        return 1

    proximoId = int(qualidades.aggregate(Max('id_qualidade'))["id_qualidade__max"]) + 1
    return proximoId

def verificaQualidade(idAnimal):
    retorno = models.Qualidade.objects.filter(id_animal=idAnimal)
    if len(retorno) > 0:
        return False
    return True