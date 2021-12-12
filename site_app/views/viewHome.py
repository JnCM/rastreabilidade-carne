from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

def index(request):
    if request.user.is_authenticated:
        return render(request, 'index.html', {"logado": 1})
    return HttpResponseRedirect("/login")
