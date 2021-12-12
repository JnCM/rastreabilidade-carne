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
            dado_hash = blockchain_connect.getDado(settings.CONTRACT, id_hash)
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
        for vacina in listaVacinas:
            if not verificaVacina(vacina):
                msg = "VACINA(s) EXISTENTE(s)"
                break
            else:
                idVacina = proximoIdVacina()
                novaVacina = models.Vacina(
                    id_vacina=idVacina,
                    especificidade=vacina['especificidade'],
                    lote=vacina['lote'],
                    dose=float(vacina['dose']),
                    data_aplicacao=vacina['data_aplicacao'],
                    id_animal=idAnimal
                )
                json_gen_hash = model_to_dict(novaVacina)
                print(json_gen_hash)
                valor_hash = hashlib.md5(str(json_gen_hash).encode())
                id_blockchain = blockchain_connect.setDado(settings.CONTRACT, settings.W3_CONNECTION, valor_hash.hexdigest())
                if id_blockchain != -1:
                    id_hash = utils.proxIdHash()
                    novoItem = models.Hash(
                        id_hash=id_hash,
                        id_tabela=3,
                        id_item=str(idVacina),
                        id_hash_blockchain=id_blockchain
                    )
                    novoItem.save(force_insert=True)
                    novaVacina.save(force_insert=True)
                    msg = "OK"
                else:
                    msg = "ERRO"
                    break
    return HttpResponse(json.dumps({'resposta': msg}))


def proximoIdVacina():
    vacinas = models.Vacina.objects.all()
    if len(vacinas) == 0:
        return 1

    proximoId = int(vacinas.aggregate(Max('id_vacina'))["id_vacina__max"]) + 1
    return proximoId

def verificaVacina(novaVacina):
    retorno = models.Vacina.objects.filter(
        especificidade=novaVacina['especificidade'],
        lote=novaVacina['lote'],
        dose=novaVacina['dose'],
        data_aplicacao=novaVacina['data_aplicacao']
    )
    if len(retorno) > 0:
        return False
    return True
