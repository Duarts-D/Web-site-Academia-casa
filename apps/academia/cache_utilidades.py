from django.core.cache import cache
from .models import Dias,CategoriaModel,TreinoDiaPadrao,TreinoDiaUser,UserDiasLista,Videos

def dias_cache_padrao_all_func(dia=None):#mudar o nome da funcao
    #Funcao para retorna Dias semanal cache ou nao cache.
    cache_dia_padrao = cache.get('cache_dia_padrao_all')
    if not cache_dia_padrao:
        cache_dia_padrao = Dias.objects.all()
        cache.set('cache_dia_padrao_all',cache_dia_padrao,(60*1440))
    if dia != None:
        cache_dia_padrao = cache_dia_padrao.filter(nome=dia).first()
        if not cache_dia_padrao:
            return False
    return cache_dia_padrao

def categorias_cache_all_func(names=None):
    #Funcao para retorna todas categorias cadastradas cache ou nao.
    cache_categorias_all = cache.get('cache_query_categorias_all')
    if not cache_categorias_all:
        cache_categorias_all = CategoriaModel.objects.all()
        cache.set('cache_query_categorias_all',cache_categorias_all,(60*1440))
    if names != None:
        cache_name_categoris_all = [objeto.categoria for objeto in cache_categorias_all]
        return cache_name_categoris_all
    return cache_categorias_all

def listas_user_dias_cache_all_func(user_id,dia=None):
    #Funcao para retorna Lista de dias do usuario cache ou nao
    cache_name_user = f'{user_id.id}-all-listas'
    cache_user_dias_lista_all = cache.get(cache_name_user)
    if not cache_user_dias_lista_all:
        cache_user_dias_lista_all  = UserDiasLista.objects.filter(user=user_id)
        if cache_user_dias_lista_all:
            cache.set(cache_name_user,cache_user_dias_lista_all,(60*30))
    if dia != None:
        cache_user_dias_lista_all = cache_user_dias_lista_all.filter(nome=dia).first()
        if not cache_user_dias_lista_all:
            return False
    return cache_user_dias_lista_all

def listas_user_dias_cache_all_delete(user,item_id=None):
    cache_name_user = f'{user.id}-all-listas'
    cache_user_dias_lista_all = cache.get(cache_name_user)
    cache_lista_nova = None
    if cache_user_dias_lista_all:
        cache_lista_nova = cache_user_dias_lista_all.exclude(id=item_id)
    if not cache_lista_nova:
        cache.delete(cache_name_user)
    else:
        cache.set(cache_name_user,cache_lista_nova,(60*60))    

def treino_dia_user_dashboard_cache_get(user,dia):
    #Funcao para retorna o videos da lista dashboard
    cache_name_treino = f'{user.id}-{dia}-video-dashboard'
    cache_treino_user = cache.get(cache_name_treino)
    if not cache_treino_user:
        cache_treino_user = TreinoDiaUser.objects.filter(user=user,dia__nome=dia)
        if not cache_treino_user:
            cache_treino_user = TreinoDiaPadrao.objects.filter(user=user,dia__nome=dia)
        if cache_treino_user:
            cache.set(cache_name_treino,cache_treino_user,(60*60))
        else:
            return False
    return cache_treino_user

def videos_cache_all_func(video_id=None,categoria=None):
    #Funcao para retorna os videos geral do site
    cache_video = cache.get('videos_all')
    if not cache_video:
        cache_video = Videos.objects.all()#colocar o filtro de publico ou nao
        cache.set('videos_all',cache_video,(60*1440))
    if video_id != None:
        cache_video = cache_video.filter(id=video_id).first()
    elif categoria != None:
        cache_video = cache_video.filter(categorias=categoria)
    return cache_video

def cache_dashboard_videos_e_categoria_delete(user,dia):
    cache_name_dashboard = f'{user.id}-{dia}-video-dashboard'
    cache.delete(cache_name_dashboard)
    cache_name_categoria = f'{user.id}-{dia}-video-players-categoria'
    cache.delete(cache_name_categoria)