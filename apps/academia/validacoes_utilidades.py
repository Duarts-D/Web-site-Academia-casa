import re
from django.core.cache import cache
import json
from .cache_utilidades import listas_user_dias_cache_all_func

def verificarString_numeros(nome):
    expressao = r'^[a-zA-Z0-9\s]*$'
    return bool(re.match(expressao,nome))

def organizarString(nome):
    return nome.strip().lower().title()



def validacao_lista(valores):
    if not valores[0] == None:
        return False
    for item in valores[1:]:
        if not item.isdigit():
            return False
    return True



def cache_exclude(cache_query,id_item,cache_name,time):
    if isinstance(cache_query, list):
        cache_query = [objeto for objeto in cache_query if int(objeto.video.id) != int(id_item)]
    else:
        cache_query = cache_query.exclude(id=id_item)
    return cache.set(cache_name,cache_query,time)

def conversorJsonParaPython(objeto):
    try:
        dados = objeto.decode('utf-8')
        objeto = json.loads(dados)
        return objeto
    except json.JSONDecodeError:
        return False
    
def itensOrgnizadoJsonTreinoView(objeto,user):
    lista_adicionar = objeto['postAdicionar']
    lista_remover = objeto['postRemove']
    dia = objeto['dia']
    if validaçaoIsdigit(lista_adicionar) and validaçaoIsdigit(lista_remover) and verificarString_numeros(dia) and verificacao_nome_query(user=user,dia=dia):
        return lista_adicionar,lista_remover,dia
    else:
        return False
    
def validaçaoIsdigit(lista):
    for item in lista:
        if not item.isdigit():
            return False
    return True

def verificacao_nome_query(user,dia):
    dia_in_lista = listas_user_dias_cache_all_func(user_id=user,dia=dia)
    if dia_in_lista:
        return True
    return False

def organizar_list_ordem(lista,ordem):
    nova_lista = []
    ordem = ordem.replace("[",'').replace("]",'')
    ordem = ordem.split(',')
    for id_ordem in ordem[1:]:
        for id_lista in lista:
            if int(id_ordem) == int(id_lista.video.id):
                nova_lista.append(id_lista)
    return nova_lista

def organizar_list_ordem_digito(lista):
    lista_int = [int(video_id) if video_id is not None and video_id.isdigit() else None for video_id in lista]
    return lista_int