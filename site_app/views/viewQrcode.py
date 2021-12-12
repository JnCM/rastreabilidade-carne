from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import json, os
from site_app.dao import models
from rastreio_carne_ufv import blockchain_connect, settings
import hashlib
import io, zipfile

def imprimir_qrcodes(request):
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
        return render(request, 'imprimir_qrcodes.html', {'animais': animais, "logado": 1})
    return HttpResponseRedirect("/login")


def get_embalagens_impressao(request):
    try:
        id_animal = request.GET.get("animal")
        embalagens = list(models.Embalagem.objects.filter(id_animal=id_animal).order_by("data_embalagem").values("id_embalagem", "tipo_corte", "peso_corte"))
        return HttpResponse(json.dumps({
            'mensagem': 'OK',
            'lista_embalagens': embalagens
        }))
    except:
        return HttpResponse(json.dumps({'mensagem': 'ERRO'}))


def baixar_qrcode(request):
    id_embalagem = request.GET.get("id_embalagem")
    qrcode = list(models.Qrcode.objects.filter(id_embalagem=id_embalagem).values())[0]
    filename = qrcode["nome_imagem"]
    content = qrcode["binario_imagem"]
    response = HttpResponse(content, content_type='image/png')
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    return response


def baixar_todas(request):
    id_animal = request.GET.get("id_animal")
    embalagens = list(models.Embalagem.objects.filter(id_animal=id_animal).order_by("data_embalagem").values("id_embalagem"))
    
    zip_dir = "qrcodes_{}".format(id_animal)
    zip_name = zip_dir + ".zip"
    zip_bytes = io.BytesIO()
    zip_file = zipfile.ZipFile(zip_bytes, "w")

    for embalagem in embalagens:
        qrcode = list(models.Qrcode.objects.filter(id_embalagem=embalagem["id_embalagem"]).values())[0]

        filename = qrcode["nome_imagem"]
        content = qrcode["binario_imagem"]
        zip_path = os.path.join(zip_dir, filename)
        zip_file.writestr(zip_path, content)
    
    zip_file.close()
    
    response = HttpResponse(zip_bytes.getvalue(), content_type="application/x-zip-compressed")
    response['Content-Disposition'] = 'attachment; filename=%s' % zip_name
    return response
