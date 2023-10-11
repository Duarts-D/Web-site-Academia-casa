import re
from django.core.cache import cache

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

def organizar_list_ordem(lista,ordem):
    nova_lista = []
    ordem = ordem.replace("'",'').replace(' ','').replace("[",'').replace("]",'')
    ordem = ordem.split(',')
    for v in ordem[1:]:
        for b in lista:
            if int(v) == int(b.video.id):
                nova_lista.append(b)
    return nova_lista

def cache_exclude(cache_query,id_item,cache_name,time):
    if isinstance(cache_query, list):
        cache_query = [objeto for objeto in cache_query if int(objeto.video.id) != int(id_item)]
    else:
        cache_query = cache_query.exclude(id=id_item)
    return cache.set(cache_name,cache_query,time)