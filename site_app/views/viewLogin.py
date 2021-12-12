from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import json
from django.contrib import auth

def login(request):
    if not request.user.is_authenticated:
        return render(request, "login.html", {})
    else:
        return HttpResponseRedirect("/")


def autenticar(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    user = auth.authenticate(username=username, password=password)

    if user is not None and user.is_active:
        request.session.set_expiry(3600)
        auth.login(request, user)
        return HttpResponse(json.dumps({"mensagem": "OK"}))
    else:
        return HttpResponse(json.dumps({"mensagem": "ERRO"}))


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/login")
