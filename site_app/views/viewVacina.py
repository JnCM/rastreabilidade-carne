from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import json
from site_app.dao import models
from site_app.utils import utils
from django.db.models import Max
from rastreio_carne_ufv import blockchain_connect, settings
import hashlib
from django.forms.models import model_to_dict

def cadastro_vacina(request):
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
        return render(request, 'cadastro_vacina.html', {'animais': animais, "logado": 1})
    return HttpResponseRedirect("/login")

def salvar_vacina(request):
    if request.method == "POST":
        idAnimal = request.POST.get("animal")
        listaVacinas = json.loads(request.POST.get("lista_vacinas"))
        i = 0
        j = 0
        tasks_ids = []
        for vacina in listaVacinas:
            if not verificaVacina(idAnimal, vacina):
                msg = "VACINA(s) EXISTENTE(s)"
                tasks_ids.append({"resposta": msg, "id_vacina": i, "task_id": -1})
            else:
                if j == 0:
                    idVacina = proximoIdVacina()
                else:
                    idVacina += 1
                novaVacina = models.Vacina(
                    id_vacina=idVacina,
                    especificidade=vacina['especificidade'],
                    lote=vacina['lote'],
                    dose=float(vacina['dose']),
                    data_aplicacao=vacina['data_aplicacao'],
                    id_animal=idAnimal
                )
                json_gen_hash = model_to_dict(novaVacina)
                valor_hash = hashlib.md5(str(json_gen_hash).encode())
                task = blockchain_connect.setDado.delay(valor_hash.hexdigest(), json_gen_hash, 3)
                msg = "OK"
                tasks_ids.append({"resposta": msg, "id_vacina": i, "task_id": task.id})
                j += 1
            i += 1
                
    return HttpResponse(json.dumps({"resposta": "OK", "tasks_ids": tasks_ids}))


def proximoIdVacina():
    vacinas = models.Vacina.objects.all()
    if len(vacinas) == 0:
        return 1

    proximoId = int(vacinas.aggregate(Max('id_vacina'))["id_vacina__max"]) + 1
    return proximoId

def verificaVacina(idAnimal, novaVacina):
    retorno = models.Vacina.objects.filter(
        especificidade=novaVacina['especificidade'],
        lote=novaVacina['lote'],
        dose=novaVacina['dose'],
        data_aplicacao=novaVacina['data_aplicacao'],
        id_animal=idAnimal
    )
    if len(retorno) > 0:
        return False
    return True
