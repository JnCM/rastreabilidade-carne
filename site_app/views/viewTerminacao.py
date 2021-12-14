from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import json
from site_app.dao import models
from site_app.utils import utils
from django.db.models import Max
from rastreio_carne_ufv import blockchain_connect, settings
import hashlib
from django.forms.models import model_to_dict


def cadastro_terminacao(request):
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
        return render(request, 'cadastro_terminacao.html', {'animais': animais, "logado": 1})
    return HttpResponseRedirect("/login")


def salvar_terminacao(request):
    if request.method == "POST":
        idAnimal = request.POST.get("animal")
        dataInicio = request.POST.get("data_inicio")
        idadeAnimal = int(request.POST.get("idade_animal"))
        pesoInicial = float(request.POST.get("peso_inicial"))
        castrado = request.POST.get("castrado")
        sistemaTerminacao = request.POST.get("sistema_terminacao")
        idTerminacao = proximoIdTerminacao()
        if not verificaTerminacao(idAnimal):
            msg = "TERMINACAO EXISTENTE"
        else:
            novaTerminacao = models.Terminacao(
                id_terminacao=idTerminacao,
                data_inicio=dataInicio,
                idade_animal=idadeAnimal,
                peso_inicial=pesoInicial,
                animal_castrado=castrado,
                sistema_terminacao=sistemaTerminacao,
                id_animal=idAnimal
            )
            json_gen_hash = model_to_dict(novaTerminacao)
            valor_hash = hashlib.md5(str(json_gen_hash).encode())
            task = blockchain_connect.setDado.delay(valor_hash.hexdigest())
            id_blockchain = task.get()
            if id_blockchain != -1:
                id_hash = utils.proxIdHash()
                novoItem = models.Hash(
                    id_hash=id_hash,
                    id_tabela=4,
                    id_item=str(idTerminacao),
                    id_hash_blockchain=id_blockchain
                )
                novoItem.save(force_insert=True)
                novaTerminacao.save(force_insert=True)
                msg = "OK"
            else:
                msg = "ERRO"
    return HttpResponse(json.dumps({'resposta': msg}))


def proximoIdTerminacao():
    terminacoes = models.Terminacao.objects.all()
    if len(terminacoes) == 0:
        return 1

    proximoId = int(terminacoes.aggregate(Max('id_terminacao'))["id_terminacao__max"]) + 1
    return proximoId

def verificaTerminacao(idAnimal):
    retorno = models.Terminacao.objects.filter(id_animal=idAnimal)
    if len(retorno) > 0:
        return False
    return True