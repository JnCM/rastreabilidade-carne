"""rastreio_carne_ufv URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import re_path
from django.contrib import admin
from site_app.views import (viewHome, viewFazenda, viewAnimal, viewVacina, viewTerminacao, viewVenda, viewQrcode,
                      viewFrigorifico, viewEmbalagem, viewAbate, viewQualidade, viewComercializacao, viewLogin, viewTask)

urlpatterns = [
    re_path(r'^login$', viewLogin.login, name='login'),
    re_path(r'^autenticar$', viewLogin.autenticar, name='autenticar'),
    re_path(r'^logout$', viewLogin.logout, name='logout'),
    re_path(r'^$', viewHome.index, name='index'),
    re_path(r'^tasks/(?P<task_id>[\w-]+)/$', viewTask.get_status, name="get_status"),
    re_path(r'^cadastro_fazenda$', viewFazenda.cadastro_fazenda, name='cadastro_fazenda'),
    re_path(r'^salvar_fazenda$', viewFazenda.salvar_fazenda, name='salvar_fazenda'),
    re_path(r'^cadastro_animal$', viewAnimal.cadastro_animal, name='cadastro_animal'),
    re_path(r'^salvar_animal$', viewAnimal.salvar_animal, name='salvar_animal'),
    re_path(r'^cadastro_vacina$', viewVacina.cadastro_vacina, name='cadastro_vacina'),
    re_path(r'^salvar_vacina$', viewVacina.salvar_vacina, name='salvar_vacina'),
    re_path(r'^cadastro_terminacao$', viewTerminacao.cadastro_terminacao, name='cadastro_terminacao'),
    re_path(r'^salvar_terminacao$', viewTerminacao.salvar_terminacao, name='salvar_terminacao'),
    re_path(r'^cadastro_venda$', viewVenda.cadastro_venda, name='cadastro_venda'),
    re_path(r'^salvar_venda$', viewVenda.salvar_venda, name='salvar_venda'),
    re_path(r'^get_itu_medio$', viewVenda.get_itu_medio, name='get_itu_medio'),
    re_path(r'^cadastro_frigorifico$', viewFrigorifico.cadastro_frigorifico, name='cadastro_frigorifico'),
    re_path(r'^salvar_frigorifico$', viewFrigorifico.salvar_frigorifico, name='salvar_frigorifico'),
    re_path(r'^cadastro_embalagem$', viewEmbalagem.cadastro_embalagem, name='cadastro_embalagem'),
    re_path(r'^salvar_embalagem$', viewEmbalagem.salvar_embalagem, name='salvar_embalagem'),
    re_path(r'^imprimir_qrcodes$', viewQrcode.imprimir_qrcodes, name='imprimir_qrcodes'),
    re_path(r'^get_embalagens_impressao$', viewQrcode.get_embalagens_impressao, name='get_embalagens_impressao'),
    re_path(r'^baixar_qrcode$', viewQrcode.baixar_qrcode, name='baixar_qrcode'),
    re_path(r'^baixar_todas$', viewQrcode.baixar_todas, name='baixar_todas'),
    re_path(r'^cadastro_abate$', viewAbate.cadastro_abate, name='cadastro_abate'),
    re_path(r'^salvar_abate$', viewAbate.salvar_abate, name='salvar_abate'),
    re_path(r'^cadastro_qualidade$', viewQualidade.cadastro_qualidade, name='cadastro_qualidade'),
    re_path(r'^salvar_qualidade$', viewQualidade.salvar_qualidade, name='salvar_qualidade'),
    re_path(r'^cadastro_comercializacao$', viewComercializacao.cadastro_comercializacao, name='cadastro_comercializacao'),
    re_path(r'^salvar_comercializacao$', viewComercializacao.salvar_comercializacao, name='salvar_comercializacao'),
    re_path(r'^embalagens/(?P<id_embalagem>[\w-]+)', viewEmbalagem.get_embalagem, name="get_embalagem"),
    re_path(r'^admin/', admin.site.urls),
]
