from .validacoes_utilidades import verificarString_numeros,validacao_lista,organizar_list_ordem_digito
from .cache_utilidades import (cache_ordem_dashboard_videos,listas_user_dias_cache_all_func,dias_cache_padrao_all_func,
                               treino_dia_user_dashboard_cache_get)
from .models import OrdemLista

class SaveOrdemQuery:
    def __init__(self,json,user):
        self.json = json
        self.user = user
        self.dia = None
        self.videos_id = None
    
    def dia_valido(self,dia):
        dias =  listas_user_dias_cache_all_func(user_id=self.user,dia=dia)
        if not dias:
            dias = dias_cache_padrao_all_func(dia=dia)
        if dias != False:
            return True
        return False
    
    def tratamento_json(self):
        dia_str_valido = verificarString_numeros(self.json.get('dia'))
        dia_query_valido = self.dia_valido(self.json.get('dia'))
        lista_videos_id = self.json.get('id')
        lista_videos_valido = validacao_lista(lista_videos_id)
        lista_lista = isinstance(lista_videos_id,list)
        if False in [dia_str_valido,dia_query_valido,lista_lista,lista_videos_valido]:
            return False
        self.dia = self.json.get('dia')
        self.videos_id = self.json.get('id')
        return True



    def verificar_query_exist_save(self):
        query_ordem = cache_ordem_dashboard_videos(user=self.user,dia=self.dia)
        if query_ordem:
            lista_ordens = organizar_list_ordem_digito(self.videos_id)
            if str(query_ordem.ordem) == str(self.videos_id):
                return True
            query_ordem.ordem = lista_ordens
            query_ordem.save()
            return True
        else:
            query = listas_user_dias_cache_all_func(self.user,self.dia)
            if not query:
                query = dias_cache_padrao_all_func(dia=self.dia)
            return query

    def save(self):
        not_erros = self.tratamento_json()

        if not_erros:
            query = self.verificar_query_exist_save()
            if not isinstance(query,bool):
                lista_ordens = organizar_list_ordem_digito(self.videos_id)
                if query._meta.model_name  == 'userdiaslista':
                    OrdemLista.objects.create(
                        ordem=lista_ordens,
                        user=self.user,
                        treinodia=query
                    )
                elif query._meta.model_name  == 'dias':
                    OrdemLista.objects.create(
                        ordem=lista_ordens,
                        user=self.user,
                        treinodiapadrao=query
                    )
            return True
        return False

                        
class DeletandoDashboardQueryVideo:
    def __init__(self,json,user):
        self.json = json
        self.user = user
        self.dia = None
        self.id = None

    def dia_valido(self,dia):
        dias =  listas_user_dias_cache_all_func(user_id=self.user,dia=dia)
        if not dias:
            dias = dias_cache_padrao_all_func(dia=dia)
        if dias != False:
            return True
        return False

    def tratamento_json(self):
        dia = self.json['dia'] if verificarString_numeros(self.json.get('dia').replace('ç','c')) else False
        id_video = self.json['id'] if (self.json.get('id')).isdigit() else False
        dia_validacao = self.dia_valido(dia)
        if dia and id_video and dia_validacao:
            self.dia = dia
            self.id = id_video
            return True
        else:
            return False
        
    def getquery(self):
        lista_query_videos = treino_dia_user_dashboard_cache_get(user=self.user,dia=self.dia)
        lista_query_videos = lista_query_videos.filter(video__id=self.id).first()
        if not lista_query_videos:
            return False
        return lista_query_videos

    def delete(self):
        not_erros = self.tratamento_json()
        if not_erros != False:
            query = self.getquery()
            if query != False:
                query.delete()
                return True
        return False
