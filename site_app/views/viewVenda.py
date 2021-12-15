from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import json
from site_app.dao import models
from site_app.utils import utils
from django.db.models import Max
from site_app.utils import db_connect as db
from rastreio_carne_ufv import blockchain_connect, settings
import hashlib
from django.forms.models import model_to_dict

def cadastro_venda(request):
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
        
        frigorificos = list(models.Frigorifico.objects.all().values())
        for frigorifico in frigorificos:
            hash_tb = list(models.Hash.objects.filter(id_tabela=7, id_item=str(frigorifico['id_frigorifico'])).values('id_hash_blockchain'))
            id_hash = hash_tb[0]['id_hash_blockchain']
            dado_hash = blockchain_connect.getDado(id_hash)
            hash_frigorifico = hashlib.md5(str(frigorifico).encode()).hexdigest()
            if hash_frigorifico == dado_hash:
                frigorifico['check_blockchain'] = True
            else:
                frigorifico['check_blockchain'] = False 
        
        return render(request, 'cadastro_venda.html', {'animais': animais, 'frigorificos': frigorificos, "logado": 1})
    return HttpResponseRedirect("/login")


def salvar_venda(request):
    if request.method == "POST":
        idFrigorifico = int(request.POST.get("frigorifico"))
        dataVenda = request.POST.get("data_venda")
        listaVendas = json.loads(request.POST.get("lista_vendas"))
        
        idVenda = proximoIdVenda()
        novaVenda = models.Venda(
            id_venda=idVenda,
            data_venda=dataVenda,
            frigorifico_comprador=idFrigorifico
        )
        json_gen_hash = model_to_dict(novaVenda)
        valor_hash = hashlib.md5(str(json_gen_hash).encode())
        task = blockchain_connect.setDado.delay(valor_hash.hexdigest(), json_gen_hash, 5)
        task_id_venda = task.id
        i = 0
        j = 0
        tasks_ids = []
        for item in listaVendas:
            if not verificaVendaAnimal(item['animal']):
                msg = "VENDA(s) EXISTENTE(s)"
                tasks_ids.append({"resposta": msg, "id_item_venda": i, "task_id": -1})
            else:
                if j == 0:
                    idItem = proximoIdItem()
                else:
                    idItem += 1
                novoItemVenda = models.VendaAnimal(
                    id_item=idItem,
                    id_venda=idVenda,
                    peso_final=float(item['peso_final']),
                    itu_min=float(item['itu_min']),
                    itu_medio=float(item['itu_medio']),
                    itu_max=float(item['itu_max']),
                    id_animal=item['animal']
                )
                json_gen_hash = model_to_dict(novoItemVenda)
                valor_hash = hashlib.md5(str(json_gen_hash).encode())
                task = blockchain_connect.setDado.delay(valor_hash.hexdigest(), json_gen_hash, 6)
                msg = "OK"
                tasks_ids.append({"resposta": msg, "id_item_venda": i, "task_id": task.id})
                j += 1
            i += 1
        
    return HttpResponse(json.dumps({"resposta": "OK", "task_id_venda": task_id_venda, "tasks_ids": tasks_ids}))


def proximoIdVenda():
    vendas = models.Venda.objects.all()
    if len(vendas) == 0:
        return 1

    proximoId = int(vendas.aggregate(Max('id_venda'))["id_venda__max"]) + 1
    return proximoId

def proximoIdItem():
    itens = models.VendaAnimal.objects.all()
    if len(itens) == 0:
        return 1

    proximoId = int(itens.aggregate(Max('id_item'))["id_item__max"]) + 1
    return proximoId

def verificaVendaAnimal(idAnimal):
    retorno = models.VendaAnimal.objects.filter(id_animal=idAnimal)
    if len(retorno) > 0:
        return False
    return True


def get_itu_medio(request):
    idAnimal = request.GET.get("animal")
    dataVenda = request.GET.get("data_venda")
    terminacao = models.Terminacao.objects.filter(id_animal=idAnimal)
    dataTerminacao = terminacao[0].data_inicio
    retorno = db.select(
        "itu_001",
        ["MIN(ITU) AS ITU_MIN, AVG(ITU) AS ITU_MEDIO, MAX(ITU) AS ITU_MAX"],
        "CAST(DATA_HORA AS DATE) >= {} AND CAST(DATA_HORA AS DATE) <= {}".format(dataTerminacao, dataVenda)
    )
    ituMinimo = retorno[0]['ITU_MIN']
    ituMedio = retorno[0]['ITU_MEDIO']
    ituMaximo = retorno[0]['ITU_MAX']
    if ituMedio == None:
        ituMedio = 0
    if ituMinimo == None:
        ituMinimo = 0
    if ituMaximo == None:
        ituMaximo = 0
    return HttpResponse(json.dumps({
        'mensagem': 'OK',
        'itu_medio': ituMedio,
        'itu_min': ituMinimo, 
        'itu_max': ituMaximo
    }))