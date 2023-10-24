from .models import TreinoDiaPadrao,TreinoDiaUser
from .cache_utilidades import videos_cache_all_func

def post_save_treinoview(selecionador,lista_treino_user_dia,query_dia,user):
    for id_video in selecionador:
        if not int(id_video) in lista_treino_user_dia:#and id_video in allvideoscadastrado
            create_treinoview(query_dia,user,int(id_video))

def post_delete_treinoview(lista_id_excluir,lista_treino_user_dia,cache_query_dashboard):
    for id_video in lista_id_excluir:
        if int(id_video) in lista_treino_user_dia:
            delete_treinoview(cache_query_dashboard,int(id_video))

def create_treinoview(query_dia,user,id_video):
    video = videos_cache_all_func(id_video)
    if query_dia._meta.model_name == 'userdiaslista':
        TreinoDiaUser.objects.create(
            dia=query_dia,
            user=user,
            video=video
        )
    else:
        TreinoDiaPadrao.objects.create(
            dia=query_dia,
            user=user,
            video=video
        )
    
def delete_treinoview(cache_query_dashboard,id_video):
    print(cache_query_dashboard,id_video)
    cache_treino = [objeto for objeto in cache_query_dashboard if objeto.video.id == id_video]
    query_treino = cache_treino[0]
    query_treino.delete()