from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import json, os, qrcode
from site_app.dao import models
from site_app.utils import utils
from django.db.models import Max
from site_app.utils import db_connect as db
from datetime import datetime
from rastreio_carne_ufv import blockchain_connect, settings
import hashlib
from django.forms.models import model_to_dict
import io

def cadastro_embalagem(request):
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
        return render(request, 'cadastro_embalagem.html', {'animais': animais, "logado": 1})
    return HttpResponseRedirect("/login")


def salvar_embalagem(request):
    if request.method == "POST":
        idAnimal = request.POST.get("animal")
        dataEmbalagem = request.POST.get("data_embalagem")
        listaEmbalagens = json.loads(request.POST.get("lista_embalagens"))
        i = 0
        j = 0
        tasks_ids = []
        for embalagem in listaEmbalagens:
            if not verificaEmbalagem(idAnimal, embalagem):
                msg = "EMBALAGEM EXISTENTE"
                tasks_ids.append({"resposta": msg, "id_embalagem": i, "task_id": -1})
            else:
                if j == 0:
                    idEmbalagem = proximoIdEmbalagem()
                else:
                    idEmbalagem += 1
                novaEmbalagem = models.Embalagem(
                    id_embalagem=idEmbalagem,
                    data_embalagem=dataEmbalagem,
                    tipo_corte=embalagem['tipo_corte'],
                    peso_corte=float(embalagem['peso_corte']),
                    id_animal=idAnimal
                )
                json_gen_hash = model_to_dict(novaEmbalagem)
                valor_hash = hashlib.md5(str(json_gen_hash).encode())
                task = blockchain_connect.setDado.delay(valor_hash.hexdigest(), json_gen_hash, 10)
                msg = "OK"
                tasks_ids.append({"resposta": msg, "id_embalagem": i, "task_id": task.id})
                j += 1
            i += 1
    return HttpResponse(json.dumps({"resposta": "OK", "tasks_ids": tasks_ids}))


def proximoIdEmbalagem():
    embalagens = models.Embalagem.objects.all()
    if len(embalagens) == 0:
        return 1

    proximoId = int(embalagens.aggregate(Max('id_embalagem'))["id_embalagem__max"]) + 1
    return proximoId

def verificaEmbalagem(idAnimal, embalagem):
    retorno = models.Embalagem.objects.filter(id_animal=idAnimal, peso_corte=float(embalagem['peso_corte']), tipo_corte=embalagem['tipo_corte'])
    if len(retorno) > 0:
        return False
    return True

def get_embalagem(request, id_embalagem):
    try:
        embalagem = list(models.Embalagem.objects.filter(id_embalagem=id_embalagem).values())
        if len(embalagem) == 0:
            return render(request, 'info_carne.html', {'mensagem': 'ERRO'})
        check_blockchain = True

        embalagem = embalagem[0]
        try:
            save_data = embalagem["data_embalagem"]
            embalagem["data_embalagem"] = embalagem["data_embalagem"].strftime("%Y-%m-%d")
            hash_tb = list(models.Hash.objects.filter(id_tabela=10, id_item=str(embalagem['id_embalagem'])).values('id_hash_blockchain'))
            id_hash = hash_tb[0]['id_hash_blockchain']
            dado_hash = blockchain_connect.getDado(id_hash)
            hash_embalagem = hashlib.md5(str(embalagem).encode()).hexdigest()
            if hash_embalagem != dado_hash:
                check_blockchain = False
                print("Erro na embalagem")
            embalagem["data_embalagem"] = save_data
        except:
            pass

        animal = list(models.Animal.objects.filter(id_animal=embalagem["id_animal"]).values())
        animal = animal[0]
        save_data = animal["data_nascimento"]
        animal["data_nascimento"] = animal["data_nascimento"].strftime("%Y-%m-%d")
        hash_tb = list(models.Hash.objects.filter(id_tabela=2, id_item=str(animal['id_animal'])).values('id_hash_blockchain'))
        id_hash = hash_tb[0]['id_hash_blockchain']
        dado_hash = blockchain_connect.getDado(id_hash)
        hash_animal = hashlib.md5(str(animal).encode()).hexdigest()
        if hash_animal != dado_hash:
            check_blockchain = False
            print("Erro no animal")
        animal["data_nascimento"] = save_data
        
        fazenda = list(models.Fazenda.objects.filter(id_fazenda=animal["id_fazenda"]).values())
        fazenda = fazenda[0]
        hash_tb = list(models.Hash.objects.filter(id_tabela=1, id_item=str(fazenda['id_fazenda'])).values('id_hash_blockchain'))
        id_hash = hash_tb[0]['id_hash_blockchain']
        dado_hash = blockchain_connect.getDado(id_hash)
        hash_fazenda = hashlib.md5(str(fazenda).encode()).hexdigest()
        if hash_fazenda != dado_hash:
            check_blockchain = False
            print("Erro na fazenda")
        
        try:
            terminacao = list(models.Terminacao.objects.filter(id_animal=animal["id_animal"]).values())
            terminacao = terminacao[0]
            save_data = terminacao["data_inicio"]
            terminacao["data_inicio"] = terminacao["data_inicio"].strftime("%Y-%m-%d")
            hash_tb = list(models.Hash.objects.filter(id_tabela=4, id_item=str(terminacao['id_terminacao'])).values('id_hash_blockchain'))
            id_hash = hash_tb[0]['id_hash_blockchain']
            dado_hash = blockchain_connect.getDado(id_hash)
            hash_terminacao = hashlib.md5(str(terminacao).encode()).hexdigest()
            if hash_terminacao != dado_hash:
                check_blockchain = False
                print("Erro na terminacao")
            terminacao["data_inicio"] = save_data
        except:
            terminacao = None
        
        try:
            qualidade = list(models.Qualidade.objects.filter(id_animal=animal["id_animal"]).values())
            qualidade = qualidade[0]
            hash_tb = list(models.Hash.objects.filter(id_tabela=9, id_item=str(terminacao['id_qualidade'])).values('id_hash_blockchain'))
            id_hash = hash_tb[0]['id_hash_blockchain']
            dado_hash = blockchain_connect.getDado(id_hash)
            hash_qualidade = hashlib.md5(str(qualidade).encode()).hexdigest()
            if hash_qualidade != dado_hash:
                check_blockchain = False
                print("Erro na qualidade")
        except:
            qualidade = None
        
        try:
            abate = list(models.Abate.objects.filter(id_animal=animal["id_animal"]).values())
            abate = abate[0]
            save_data = abate["data_abate"]
            abate["data_abate"] = abate["data_abate"].strftime("%Y-%m-%d")
            hash_tb = list(models.Hash.objects.filter(id_tabela=8, id_item=str(abate['id_abate'])).values('id_hash_blockchain'))
            id_hash = hash_tb[0]['id_hash_blockchain']
            dado_hash = blockchain_connect.getDado(id_hash)
            hash_abate = hashlib.md5(str(abate).encode()).hexdigest()
            if hash_abate != dado_hash:
                check_blockchain = False
                print("Erro no abate")
            abate["data_abate"] = save_data
        except:
            abate = None
        
        try:
            vacinas = list(models.Vacina.objects.filter(id_animal=animal["id_animal"]).values())
            for vacina in vacinas:
                save_data = vacina["data_aplicacao"]
                vacina["data_aplicacao"] = vacina["data_aplicacao"].strftime("%Y-%m-%d")
                hash_tb = list(models.Hash.objects.filter(id_tabela=3, id_item=str(vacina['id_vacina'])).values('id_hash_blockchain'))
                id_hash = hash_tb[0]['id_hash_blockchain']
                dado_hash = blockchain_connect.getDado(id_hash)
                hash_vacina = hashlib.md5(str(vacina).encode()).hexdigest()
                if hash_vacina != dado_hash:
                    check_blockchain = False
                    print("Erro na vacina {}".format(vacina["id_vacina"]))
                vacina["data_aplicacao"] = save_data
        except:
            vacinas = None
        
        try:
            itemVenda = list(models.VendaAnimal.objects.filter(id_animal=animal["id_animal"]).values())
            itemVenda = itemVenda[0]
            hash_tb = list(models.Hash.objects.filter(id_tabela=6, id_item=str(itemVenda['id_item'])).values('id_hash_blockchain'))
            id_hash = hash_tb[0]['id_hash_blockchain']
            dado_hash = blockchain_connect.getDado(id_hash)
            hash_item_venda = hashlib.md5(str(itemVenda).encode()).hexdigest()
            if hash_item_venda != dado_hash:
                check_blockchain = False
                print("Erro no item da venda")
        except:
            itemVenda = None
        
        try:
            venda = list(models.Venda.objects.filter(id_venda=itemVenda["id_venda"]).values())
            venda = venda[0]
            save_data = venda["data_venda"]
            venda["data_venda"] = venda["data_venda"].strftime("%Y-%m-%d")
            hash_tb = list(models.Hash.objects.filter(id_tabela=5, id_item=str(venda['id_venda'])).values('id_hash_blockchain'))
            id_hash = hash_tb[0]['id_hash_blockchain']
            dado_hash = blockchain_connect.getDado(id_hash)
            hash_venda = hashlib.md5(str(venda).encode()).hexdigest()
            if hash_venda != dado_hash:
                check_blockchain = False
                print("Erro na venda")
            venda["data_venda"] = save_data
        except:
            venda = None
        
        try:
            frigorifico = list(models.Frigorifico.objects.filter(id_frigorifico=venda["frigorifico_comprador"]).values())
            frigorifico = frigorifico[0]
            hash_tb = list(models.Hash.objects.filter(id_tabela=7, id_item=str(frigorifico['id_frigorifico'])).values('id_hash_blockchain'))
            id_hash = hash_tb[0]['id_hash_blockchain']
            dado_hash = blockchain_connect.getDado(id_hash)
            hash_frigorifico = hashlib.md5(str(frigorifico).encode()).hexdigest()
            if hash_frigorifico != dado_hash:
                check_blockchain = False
                print("Erro no frigorifico")
        except:
            frigorifico = None

        dataEmbalagem = embalagem["data_embalagem"]
        try:
            comercializacao_embalagem = list(models.ComercializacaoEmbalagem.objects.filter(id_embalagem=embalagem["id_embalagem"]).values())
            comercializacao_embalagem = comercializacao_embalagem[0]
            hash_tb = list(models.Hash.objects.filter(id_tabela=12, id_item=str(comercializacao_embalagem['id_item'])).values('id_hash_blockchain'))
            id_hash = hash_tb[0]['id_hash_blockchain']
            dado_hash = blockchain_connect.getDado(id_hash)
            hash_com_emb = hashlib.md5(str(comercializacao_embalagem).encode()).hexdigest()
            if hash_com_emb != dado_hash:
                check_blockchain = False
                print("Erro na comercializacao emb")

            comercializacao = list(models.Comercializacao.objects.filter(id_comercializacao=comercializacao_embalagem["id_comercializacao"]).values())
            comercializacao = comercializacao[0]
            save_data = comercializacao["data_venda"]
            comercializacao["data_venda"] = comercializacao["data_venda"].strftime("%Y-%m-%dT%H:%M")
            hash_tb = list(models.Hash.objects.filter(id_tabela=11, id_item=str(comercializacao['id_comercializacao'])).values('id_hash_blockchain'))
            id_hash = hash_tb[0]['id_hash_blockchain']
            dado_hash = blockchain_connect.getDado(id_hash)
            hash_com = hashlib.md5(str(comercializacao).encode()).hexdigest()
            if hash_com != dado_hash:
                check_blockchain = False
                print("Erro na comercializacao")
            comercializacao["data_venda"] = save_data
            dataVenda = comercializacao["data_venda"]
        except:
            dataVenda = datetime.now()
        
        retorno = db.select(
            "refrigerador_001",
            ["AVG(TEMP) AS TEMP_MEDIA"],
            "DATA_HORA >= '{}' AND DATA_HORA <= '{}'".format(datetime(dataEmbalagem.year, dataEmbalagem.month, dataEmbalagem.day), dataVenda)
        )
        tempMedia = retorno[0]['TEMP_MEDIA']
        if tempMedia == None:
            tempMedia = 0
        else:
            tempMedia = round(float(tempMedia), 2)
        
        return render(
            request,
            'info_carne.html',
            {
                'mensagem': 'OK',
                'animal': animal,
                'fazenda': fazenda,
                'terminacao': terminacao,
                'qualidade': qualidade,
                'abate': abate,
                'vacinas': vacinas,
                'item_venda': itemVenda,
                'venda': venda,
                'frigorifico': frigorifico,
                'embalagem': embalagem,
                'temperatura_media': tempMedia,
                'valido_blockchain': check_blockchain
            })
    except:
        return render(request, 'info_carne.html', {'mensagem': 'ERRO'})
