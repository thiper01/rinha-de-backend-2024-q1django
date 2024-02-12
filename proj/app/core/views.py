import asyncio
from django.shortcuts import render
from .models import Transacoes, Clientes, Saldos, get_info
from django.http import HttpRequest, HttpResponse, JsonResponse

def home(request):
    return render(request, "index.html")

def transacoes(request, id):
    if request.method == "POST":
        #cliente = id
        valorTrs = request.POST.get("valor")
        tipo = request.POST.get("tipo")
        descr = request.POST.get("descricao")

        cliente, saldo = asyncio.run(get_info(id))
        # cliente = Clientes.objects.get(id=id)
        # saldo = Saldos.objects.get(cliente=id).valor

        if tipo == "d":
            if saldo.valor-valorTrs < cliente.limite:
                response = HttpResponse
                response.status_code = 422
                return response
            else:
                saldo.valor -= valorTrs
                saldo.save()
        
        Transacoes.objects.create(cliente=id, valor=valorTrs, tipo=tipo, descricao=descr)
        response = JsonResponse({
            "limite": cliente.limite,
            "saldo": saldo})
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
