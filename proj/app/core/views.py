from django.shortcuts import render
from .models import Transacoes, Clientes, Saldos
from django.http import HttpRequest, HttpResponse, JsonResponse

def home(request):
    return render(request, "index.html")

def transacoes(request, id):
    if request.method == "POST":
        #cliente = id
        valor = request.POST.get("valor")
        tipo = request.POST.get("tipo")
        descr = request.POST.get("descricao")
        
        Transacoes.objects.create(cliente=id, valor=valor, tipo=tipo, descricao=descr)
        response = JsonResponse({
            "limite": "",
            "saldo": ""})
        response.status_code = 200
        return response
    else:
        response = HttpResponse
        response.status_code = 400
        return response

def extrato(request, id):
    if request.method == "GET":
        response = JsonResponse({
            "limite": "",
            "saldo": ""})
        return response
    else:
        response = HttpResponse
        response.status_code = 400
        return response
# Create your views here.
