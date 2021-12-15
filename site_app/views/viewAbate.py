from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import json
from site_app.dao import models
from site_app.utils import utils
from django.db.models import Max
from rastreio_carne_ufv import blockchain_connect, settings
import hashlib
from django.forms.models import model_to_dict


def cadastro_abate(request):
    if request.user.is_authenticated:
        animais = list(models.Animal.objects.all().values())
        for animal in animais:
            animal["data_nascimento"] = animal["data_nascimento"].strftime("%Y-%m-%d")
            hash_tb = list(models.Hash.objects.filter(id_tabela=2, id_item=str(animal['id_animal'])).values('id_hash_blockchain'))
            id_hash = hash_tb[0]['id_hash_blockchain']
            dado_hash = blockchain_connect.getDado(id_hash)
            hash_animal = hashlib.md5(str(animal).encode()).hexdigest()
            if hash_animal == dado_hash:
                animal['check_blockchain'] = True
            else:
                animal['check_blockchain'] = False
        return render(request, 'cadastro_abate.html', {'animais': animais, "logado": 1})
    return HttpResponseRedirect("/login")


def salvar_abate(request):
    if request.method == "POST":
        idAnimal = request.POST.get("animal")
        dataAbate = request.POST.get("data_abate")
        phInicial = float(request.POST.get("ph_inicial"))
        phFinal = float(request.POST.get("ph_final"))
        gordura = float(request.POST.get("gordura_subcutanea"))
        pesoQuenteE = float(request.POST.get("peso_carcaca_quente_esquerda"))
        pesoQuenteD = float(request.POST.get("peso_carcaca_quente_direita"))
        pesoFrioE = float(request.POST.get("peso_carcaca_frio_esquerda"))
        pesoFrioD = float(request.POST.get("peso_carcaca_frio_direita"))
        idAbate = proximoIdAbate()
        if not verificaAbate(idAnimal):
            msg = "ABATE EXISTENTE"
            task_id = -1
        else:
            novoAbate = models.Abate(
                id_abate=idAbate,
                data_abate=dataAbate,
                ph_inicial=phInicial,
                ph_final=phFinal,
                gordura_subcutanea=gordura,
                peso_carcaca_quente_esquerda=pesoQuenteE,
                peso_carcaca_quente_direita=pesoQuenteD,
                peso_carcaca_frio_esquerda=pesoFrioE,
                peso_carcaca_frio_direita=pesoFrioD,
                id_animal=idAnimal
            )
            json_gen_hash = model_to_dict(novoAbate)
            valor_hash = hashlib.md5(str(json_gen_hash).encode())
            task = blockchain_connect.setDado.delay(valor_hash.hexdigest(), json_gen_hash, 8)
            task_id = task.id 
            msg = "OK"
    return HttpResponse(json.dumps({'resposta': msg, "task_id": task_id}))


def proximoIdAbate():
    abates = models.Abate.objects.all()
    if len(abates) == 0:
        return 1

    proximoId = int(abates.aggregate(Max('id_abate'))["id_abate__max"]) + 1
    return proximoId

def verificaAbate(idAnimal):
    retorno = models.Abate.objects.filter(id_animal=idAnimal)
    if len(retorno) > 0:
        return False
    return True