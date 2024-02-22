import asyncio
import json
from .models import Transacoes, get_info, get_info
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.core.exceptions import ValidationError


def transacoes(request, id):
    if request.method == "POST":
        try:
            body = json.loads(request.body)
        except:
            response = HttpResponse()
            response.status_code = 422
            return response
        
        valor_tran = body["valor"]
        tipo = body["tipo"]
        descr = body["descricao"]
        try:
            # cliente = Clientes.objects.get(id=id)
            # saldo = Saldos.objects.get(cliente=id).valor
            cliente, saldo = asyncio.run(get_info(id))
        except:
            response = HttpResponse()
            response.status_code = 404
            return response

        transacao = Transacoes(cliente=cliente, valor=valor_tran, tipo=tipo, descricao=descr)
        try:
            transacao.clean_fields(exclude=["cliente","realizada_em"])
        except ValidationError as e:
            erro = " \n".join(e.messages)
            response = HttpResponse(erro)
            response.status_code = 422
            return response

        if tipo == "d":
            if (saldo.valor+cliente.limite)-valor_tran < 0:
                response = HttpResponse()
                response.status_code = 422
                return response
            else:
                saldo.valor -= valor_tran
                saldo.save()
        
        transacao.save()
        response = JsonResponse({
            "limite": cliente.limite,
            "saldo": saldo.valor})
        response.status_code = 200
        return response
    
    else:
        response = HttpResponse()
        response.status_code = 400
        return response

def extrato(request, id):
    if request.method == "GET":
        try:
            # cliente = Clientes.objects.get(id=id)
            # saldo = Saldos.objects.get(cliente=id)
            cliente, saldo = asyncio.run(get_info(id))
        except:
            response = HttpResponse()
            response.status_code = 404
            return response
            
        last_tran = list(Transacoes.objects.filter(cliente=id).order_by("realizada_em")[:10].values("valor", "tipo", "descricao", "realizada_em"))
        response = JsonResponse(
            {
                "saldo": {
                    "total": saldo.valor,
                    "data_extrato": timezone.now(),
                    "limite": cliente.limite
                },
                "ultimas_transacoes": last_tran
            })
        response.status_code = 200
        return response
    else:
        response = HttpResponse()
        response.status_code = 400
        return response
