from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import json
from site_app.dao import models
from site_app.utils import utils
from rastreio_carne_ufv import blockchain_connect, settings
import hashlib
from django.forms.models import model_to_dict

def cadastro_animal(request):
    if request.user.is_authenticated:
        fazendas = list(models.Fazenda.objects.all().values())
        for fazenda in fazendas:
            hash_tb = list(models.Hash.objects.filter(id_tabela=1, id_item=str(fazenda['id_fazenda'])).values('id_hash_blockchain'))
            id_hash = hash_tb[0]['id_hash_blockchain']
            dado_hash = blockchain_connect.getDado(settings.CONTRACT, id_hash)
            hash_fazenda = hashlib.md5(str(fazenda).encode()).hexdigest()
            if hash_fazenda == dado_hash:
                fazenda['check_blockchain'] = True
            else:
                fazenda['check_blockchain'] = False    

        return render(request, 'cadastro_animal.html', {'fazendas': fazendas, "logado": 1})
    return HttpResponseRedirect("/login")


def salvar_animal(request):
    if request.method == "POST":
        idAnimal = request.POST.get("id_animal")
        racaAnimal = request.POST.get("raca_animal")
        generoAnimal = request.POST.get("genero_animal")
        dataNascimento = request.POST.get("data_nascimento")
        pesoNascimento = float(request.POST.get("peso_nascimento"))
        idFazenda = int(request.POST.get("fazenda"))
        if not verificaAnimal(idAnimal):
            msg = "ANIMAL EXISTENTE"
        else:
            novoAnimal = models.Animal(
                id_animal=idAnimal,
                raca=racaAnimal,
                genero=generoAnimal,
                data_nascimento=dataNascimento,
                peso_nascimento=pesoNascimento,
                id_fazenda=idFazenda
            )
            json_gen_hash = model_to_dict(novoAnimal)
            valor_hash = hashlib.md5(str(json_gen_hash).encode())
            task = blockchain_connect.setDado.delay(valor_hash.hexdigest())
            id_blockchain = task.get()
            if id_blockchain != -1:
                id_hash = utils.proxIdHash()
                novoItem = models.Hash(
                    id_hash=id_hash,
                    id_tabela=2,
                    id_item=idAnimal,
                    id_hash_blockchain=id_blockchain
                )
                novoItem.save(force_insert=True)
                novoAnimal.save(force_insert=True)
                msg = "OK"
            else:
                msg = "ERRO"
    return HttpResponse(json.dumps({'resposta': msg}))


def verificaAnimal(idAnimal):
    retorno = models.Animal.objects.filter(id_animal=idAnimal)
    if len(retorno) > 0:
        return False
    return True
