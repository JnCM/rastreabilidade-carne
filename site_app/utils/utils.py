from site_app.dao import models
from django.db.models import Max

def proxIdHash():
    hashes = models.Hash.objects.all()
    if len(hashes) == 0:
        return 1

    proximoId = int(hashes.aggregate(Max('id_hash'))["id_hash__max"]) + 1
    return proximoId
