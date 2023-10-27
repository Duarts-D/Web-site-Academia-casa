from typing import Any, Dict
from django.db.models.query import QuerySet
from django.http import HttpRequest,HttpResponse
from django.shortcuts import render,redirect,reverse
from django.views.generic import ListView
from .models import Videos,TreinoDiaPadrao,Dias,CategoriaModel,UserDiasLista,TreinoDiaUser,OrdemLista
import json
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from .validacoes_utilidades import (verificarString_numeros,organizarString,validacao_lista,cache_exclude,
                                    conversorJsonParaPython,itensOrgnizadoJsonTreinoView,verificacao_nome_query,
                                    organizar_list_ordem,organizar_list_ordem_digito)
from .cache_utilidades import (dias_cache_padrao_all_func,categorias_cache_all_func,listas_user_dias_cache_all_func,
                               treino_dia_user_dashboard_cache_get,videos_cache_all_func,cache_dashboard_videos_e_categoria_delete,
                               listas_user_dias_cache_all_delete,cache_ordem_dashboard_videos,cache_ordem_dashboard_videos_delete,cache_ordem_dashboard_videos_reoganizar)
from django.core.cache import cache
from .salve_utilidade import post_save_treinoview,post_delete_treinoview
from .utilidades_ExercicioDashboard import SaveOrdemQuery,DeletandoDashboardQueryVideo


class CustomContextMixin(ListView):
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        get = super().get_context_data(**kwargs)
        get['geral'] = 'Geral'
        return get
    
class HomePageView(ListView):#cache
    template_name = 'index.html'
    def setup(self,*args,**kwargs):
        cache.clear() ## Limpar cache
        super().setup(*args,**kwargs)
        self.contexto = {'geral':'Geral',}

    def get(self,*args,**kwargs):
        return render(self.request,self.template_name,self.contexto)

class ListasView(LoginRequiredMixin,CustomContextMixin,ListView):#cache
    template_name = 'listas.html'
    model = Dias
    context_object_name = 'dia_semana_index'
    login_url = "login"
    redirect_field_name ='redirect_to'
    
    def get_queryset(self) -> QuerySet[Any]:
        #cache
        qs_cache = dias_cache_padrao_all_func()
        return qs_cache
    
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        get =  super().get_context_data(**kwargs)
        #cache
        cache_listas = listas_user_dias_cache_all_func(user_id=self.request.user)
        get['listas'] = cache_listas
        return get
    
    def post(self,*args,**kwargs):
        json = conversorJsonParaPython(self.request.body)
        user = self.request.user
        cache_listas = listas_user_dias_cache_all_func(user_id=user)
        if json != False and json.get('remove'):
            #cache
            # Delete item lista por post js
            id_remover_query = json.get('remove')
            if id_remover_query and id_remover_query.isdigit():
                query_para_remover = cache_listas.filter(id=id_remover_query)
                if query_para_remover:
                    query_para_remover.delete()
                    listas_user_dias_cache_all_delete(user,int(id_remover_query))
                return JsonResponse({'remover': True})

        
        #Criar lista do usuario por post js
        if json != False and json.get('nome'):
            string_valido = verificarString_numeros(json['nome'])
            if string_valido:
                nome = organizarString(json['nome'])
                if len(cache_listas) != 10:  #and isinstance(cache_query, QuerySet)#maximo 10 de lista
                    create_query = UserDiasLista.objects.create(nome=nome,user=user)
                    listas_user_dias_cache_all_delete(user)#removendo cache
                    return JsonResponse({'id':create_query.id,'nome':create_query.nome})

        return JsonResponse({'erro':'Algo deu errado'},status=500)
            

class ExercicioDashboard(LoginRequiredMixin,CustomContextMixin,ListView):#cache
    model = TreinoDiaPadrao
    template_name = 'dashboard.html'
    context_object_name = 'dia_semana'
    paginate_by = 50
    ordering = ('-id')


    def setup(self, request: HttpRequest, *args: Any, **kwargs: Any) -> None:
        setup = super().setup(request, *args, **kwargs)
        self.dia = self.kwargs.get('dia')

        if self.dia is None:
            #TODO arruma logica para bloquear o acesso a pagina e retona 400
            return redirect('listas')  
        
        self.user = self.request.user
        self.categoria = self.kwargs.get('categoria')
        return setup
    

    def get_queryset(self):
        #cache
        cache_dashboard_treino= treino_dia_user_dashboard_cache_get(self.user,self.dia)
        
        # print(cache_dashboard_treino)
        if cache_dashboard_treino == False:
            return []

        if self.categoria == 'Geral':
            cache_ordem_string = cache_ordem_dashboard_videos(user=self.user,dia=self.dia)
            if cache_ordem_string:
                try:
                    ordem_Nova = organizar_list_ordem(cache_dashboard_treino,cache_ordem_string.ordem)
                    qs  = sorted(cache_dashboard_treino,
                        key=lambda x: ordem_Nova.index(x) if x in ordem_Nova else len(ordem_Nova))
                except ValueError:
                    return cache_dashboard_treino 
                
                if qs:
                    return qs
            return cache_dashboard_treino

        if self.categoria != 'Geral':
            cache_query_dashboard = cache_dashboard_treino.filter(video__categorias__categoria__icontains=self.categoria)
        
        return cache_query_dashboard
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        get = super().get_context_data(**kwargs)
        get['dia'] = self.dia

        lista_dia_page = []
        for categoria in get['dia_semana']:
            categorias = categoria.video.categorias
            lista_dia_page.append(categorias)
        categorias = set(lista_dia_page)
        
        get['categorias'] = categorias
        return get

    
    def post(self,*args,**kwargs):
        json = conversorJsonParaPython(self.request.body)
        
        if json:
            dia = json.get('dia')
            lista_ids_videos = json.get('id')
            if dia and isinstance(lista_ids_videos,list):#Salvando query ordem
                salve = SaveOrdemQuery(json=json,user=self.user)
                resultado = salve.save()
                if resultado:
                    #Deletando cache ordem Lista
                    cache_ordem_dashboard_videos_reoganizar(self.user,json['dia'],json['id'])
                    return JsonResponse({'mensagem': 'Dados recebidos com sucesso'})
                else:
                    return JsonResponse({'erro': 'Dados inválido'}, status=400)
            else:
                #Deletando query
                query = DeletandoDashboardQueryVideo(json=json,user=self.user)
                resultado = query.delete()
                if resultado:
                    #cache
                    cache_dashboard_videos_e_categoria_delete(user=self.user,dia=json['dia'],id_video=json['id'])
                    return JsonResponse({'mensagem': 'Dados recebidos com sucesso'})
                else:
                    return JsonResponse({'mensagem': 'Dados recebidos com sucesso'})

        else:
            return JsonResponse({'erro': 'Formato JSON inválido'}, status=400)
    
class TreinoView(LoginRequiredMixin,CustomContextMixin,ListView):#cache
    model = Videos
    template_name = 'criartreino.html'
    context_object_name = 'videos'
    paginate_by = 50
    ordering = ('id')
    login_url = "login"
    redirect_field_name ='redirect_to'

    def setup(self,*args,**kwargs):
        setup = super().setup(*args,**kwargs)

        self.dia = self.kwargs.get('dia')
        self.user = self.request.user
        
        self.categoria = self.kwargs.get('categoria')
        print(self.categoria)
        print(self.dia)

        self.treino_user_dia_lista = []
    
        self.cache_query_listas = listas_user_dias_cache_all_func(self.user)

        # if self.cache_query_listas:
        #     dia = self.cache_query_listas.filter(nome=self.dia)
        #     if not dia:
        #         raise ValueError#TODO fazer pagina html error 400

        self.cache_query_dashboard = treino_dia_user_dashboard_cache_get(self.user,self.dia)
        self.cache_query_videos_all = videos_cache_all_func()
        self.cache_query_name_categoris_all = categorias_cache_all_func(names=True)
        
        if self.cache_query_dashboard:
            for id_video in self.cache_query_dashboard :
                self.treino_user_dia_lista.append(id_video.video.id)

        return setup

    def get_queryset(self):
        if self.cache_query_videos_all:
            if isinstance(self.cache_query_videos_all,QuerySet) and self.categoria in self.cache_query_name_categoris_all:
                cache = self.cache_query_videos_all.filter(categorias__categoria=self.categoria)
                return cache
            return self.cache_query_videos_all
        else:
            return super().get_queryset()
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        get_contexto = super().get_context_data(**kwargs)
        get_contexto['dia'] = self.dia
        get_contexto['lista_treino'] = True
        get_contexto['lista_video_id'] = self.treino_user_dia_lista
        get_contexto['categorias'] = self.cache_query_name_categoris_all
        get_contexto['categoria_listagem'] = self.categoria

        return get_contexto
    
    def post(self,request,*args,**kwargs):
        json = conversorJsonParaPython(self.request.body)
        selecionador = self.request.POST.getlist('videos')

        #cache
        cache_dia_padrao = dias_cache_padrao_all_func()
        cache_name_categoris_all = self.cache_query_name_categoris_all
        

        if json:
            listas = itensOrgnizadoJsonTreinoView(objeto=json,user=self.user)
            if listas != False :
                selecionador = listas[0]
                listaRemover = listas[1]
                dia = listas[2]
                query_dia = cache_dia_padrao.filter(nome=dia).first()

                if not query_dia:
                    query_dia = self.cache_query_listas.filter(nome=dia).first()

                post_save_treinoview(selecionador=selecionador,lista_treino_user_dia=self.treino_user_dia_lista,query_dia=query_dia,user=self.user)
                post_delete_treinoview(lista_id_excluir=listaRemover,lista_treino_user_dia=self.treino_user_dia_lista,cache_query_dashboard=self.cache_query_dashboard)

                cache_dashboard_videos_e_categoria_delete(self.user,dia)
                # cache_ordem_dashboard_videos_delete(self.user,dia)
                return JsonResponse({'mensagem': 'Dados recebidos com sucesso'},status=200)
            return JsonResponse({'erro': 'Invalido indice.'}, status=400)
        
        #retorno da funcao
        query_dia = cache_dia_padrao.filter(nome=self.dia).first()

        if not query_dia:
            query_dia = self.cache_query_listas.filter(nome=self.dia).first()

        categoria = self.categoria
        pagina_1 = self.request.POST.get('pagina_1')
        pagina_2 = self.request.POST.get('pagina_2')
        pagina_final = self.request.POST.get('pagina_final')
        pagina_4 = self.request.POST.get('pagina_4')

        # lista_page = self.request.POST.getlist('id_page')
        
        if self.categoria != 'Geral' and self.categoria in cache_name_categoris_all:
            videos_all_categoria = self.cache_query_videos_all.filter(categorias__categoria=self.categoria)
            lista_ids_videos = [objeto.id for objeto in videos_all_categoria]
            lista_ids_videos_excluir = [objeto for objeto in lista_ids_videos if not str(objeto) in selecionador]
            
            post_save_treinoview(selecionador=selecionador,lista_treino_user_dia=self.treino_user_dia_lista,
                                 query_dia=query_dia,user=self.user)
   
            post_delete_treinoview(lista_id_excluir=lista_ids_videos_excluir,lista_treino_user_dia=self.treino_user_dia_lista,
                    cache_query_dashboard=self.cache_query_dashboard)
        else:
            if len(selecionador) >=1 :
                post_save_treinoview(selecionador=selecionador,lista_treino_user_dia=self.treino_user_dia_lista,
                        query_dia=query_dia,user=self.user)

                # if len(self.treino_user_dia_lista) >= 1:
                #     if len(lista_page)>=1:
                #         lista_page.remove(str(id_video))
                #     else:
                #         if not int(id_video) in self.treino_user_dia_lista:
                #             self.treino_user_dia_lista.append(id_video)

            lista_id_excluir =  [ x for x in self.treino_user_dia_lista if str(x) not in selecionador ]
            
            post_delete_treinoview(lista_id_excluir=lista_id_excluir,lista_treino_user_dia=self.treino_user_dia_lista,
                    cache_query_dashboard=self.cache_query_dashboard)
            
        cache_dashboard_videos_e_categoria_delete(self.user,self.dia)
        # cache_ordem_dashboard_videos_delete(self.user,self.dia)

        a = self.request.POST.get('todos')
        if not pagina_1 is None:
            pagina_1 = int(pagina_1)-1
            pagina = pagina_1
        elif not pagina_2 is None:
            pagina_2 = int(pagina_2)+1
            pagina = pagina_2
        elif not pagina_final is None:
            pagina = pagina_final
        elif not pagina_4 is None:
            pagina = 1
        else:
            cat = self.request.POST.get('categorias__input')

            if not a is None:
                url = reverse('lista_treino',kwargs={'dia':self.dia,'categoria':self.dia})
                return redirect(url)
            if cat is None:
                url = reverse('exercicios',kwargs={'dia':self.dia,'categoria':'Geral'})
                return redirect(url)
                # return redirect(request.META.get('HTTP_REFERER', '/'))
            else:
                url = reverse('lista_treino',kwargs={'dia':self.dia,'categoria':cat})
                return redirect(url)
        url = reverse('lista_treino',kwargs={'dia':self.dia,'categoria':categoria}) + f'?page={pagina}'

        return redirect(url)
        

class TodosVideosView(CustomContextMixin,ListView):#cache
    model = Videos
    context_object_name = 'videos'
    template_name = 'videos.html'
    paginate_by = 50
    ordering = ('-id')

    def get_queryset(self):
        cache_videos_all = cache.get('videos_all')
        #cache
        if cache_videos_all:
            return cache_videos_all
        else:
            qs = super().get_queryset()
            cache.set('videos_all',qs,(60*1440))
            # categoria = self.kwargs.get('categorias')
            return qs

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        get = super().get_context_data(**kwargs)
        get['dia'] = False
        get['geral'] = 'Geral'
        cache_categorias_all = cache.get('cache_query_categoria_all')
        if cache_categorias_all:
            get['categorias'] = cache_categorias_all
        else:
            categoria = CategoriaModel.objects.all()
            get['categorias'] = categoria
            cache.set('cache_query_categoria_all',categoria,(60*1440))
        return get
        # get['categorias'] = CategoriaModel.objects.all()

class VideosZumba(CustomContextMixin,ListView):#cache
    model = Videos
    context_object_name = 'videos'
    template_name = 'videos_zumba.html'
    paginate_by = 50
    ordering = ('-id')

    def get_queryset(self) -> QuerySet[Any]:
        cache_videos_all = cache.get('videos_all')
        
        #cache
        if cache_videos_all:
            return cache_videos_all.filter(categorias__categoria='Zumba')
        
        qs = super().get_queryset()
        qs = qs.filter(categorias__categoria='Zumba')
        return qs 
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        get = super().get_context_data(**kwargs)
        get['dia'] = False
        get['zumba'] = True
        return get
