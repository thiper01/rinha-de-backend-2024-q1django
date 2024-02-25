import asyncio
from django.core.cache import cache
from .models import Clientes, Saldos


def get_cliente(key):
    cached_cliente = cache.get(str(key))
    if cached_cliente is not None:
        return cached_cliente
    
    cliente = Clientes.objects.get(id=key)
    cache.set(str(key) , cliente, 3600)
    return cliente

async def get_info_async(id):
    async with asyncio.TaskGroup() as tg:
        gcli = tg.create_task(Clientes.objects.aget(id=id))
        gsald = tg.create_task(Saldos.objects.aget(cliente=id))
    return gcli.result(), gsald.result()

def get_info(id):
    cached_cliente = cache.get(str(id))
    if cached_cliente is not None:
        saldo = Saldos.objects.get(cliente=id)
        return cached_cliente, saldo
    
    cliente, saldo = asyncio.run(get_info_async(id))
    cache.set(str(id) , cliente, 3600)
    return cliente, saldo
