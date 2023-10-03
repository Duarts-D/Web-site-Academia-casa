from typing import Any, Dict
from django import http
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render,redirect,reverse
from django.views import View
from django.views.generic import ListView
from .models import Videos,TreinoDiaPadrao,Dias,CategoriaModel,UserDiasLista,TreinoDiaUser,OrdemLista
from django.contrib.auth.models import User
import json
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from .utilidades import verificarString_numeros,organizarString,validacao_lista,organizar_list_ordem

class CustomContextMixin(ListView):


    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        get = super().get_context_data(**kwargs)
        get['geral'] = 'Geral'
        return get

class HomePageView(ListView):
    template_name = 'index.html'

    def setup(self,*args,**kwargs):
        super().setup(*args,**kwargs)
        self.contexto = {'geral':'Geral',}

    def get(self,*args,**kwargs):
        return render(self.request,self.template_name,self.contexto)

class ListasView(LoginRequiredMixin,CustomContextMixin,ListView):
    template_name = 'listas.html'
    model = Dias
    context_object_name = 'dia_semana_index'
    login_url = "login"
    redirect_field_name ='redirect_to'
    

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        get =  super().get_context_data(**kwargs)
        get['listas'] = UserDiasLista.objects.filter(user=self.request.user)
        return get
    
    def post(self,*args,**kwargs):
        dados_em_bytes = self.request.body
        dados_em_string = dados_em_bytes.decode('utf-8')
        dados_dict = json.loads(dados_em_string)

        #Delete item lista por post js
        if dados_dict.get('remove'):
            if dados_dict['remove'].isdigit():
                idlista = dados_dict['remove']
                remover = UserDiasLista.objects.filter(user=self.request.user,id=idlista)
                if remover:
                    remover.delete()
                    return JsonResponse({'remover': True})

        
        #Criar lista do usuario por post js
        if dados_dict.get('nome'):
            quantidade = UserDiasLista.objects.filter(user=self.request.user)
            if len(quantidade) != 10: #maximo 10 de lista
                string = verificarString_numeros(dados_dict['nome'])
                if string:
                    nome = dados_dict['nome']
                    nome = organizarString(nome)
                    item = UserDiasLista.objects.create(nome=nome,user=self.request.user)
                    return JsonResponse({'id':item.id,'nome':item.nome})

        return JsonResponse({'erro':'Algo deu errado'},status=500)
            

class ExercicioSemanaView(LoginRequiredMixin,CustomContextMixin,ListView):
    model = TreinoDiaPadrao
    template_name = 'dashboard.html'
    context_object_name = 'dia_semana'
    paginate_by = 50
    ordering = ('-id')


    def setup(self, request: HttpRequest, *args: Any, **kwargs: Any) -> None:
        setup = super().setup(request, *args, **kwargs)
        self.dia = self.kwargs.get('dia')
        self.user = self.request.user
        self.categoria = self.kwargs.get('categoria')
        return setup
    

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        categoria = self.categoria
        if categoria == 'Geral':
                qs = TreinoDiaUser.objects.filter(user=user,dia__nome=self.dia)
                if not qs :
                    qs = TreinoDiaPadrao.objects.filter(user=user,dia__nome=self.dia)

                ordem_string = OrdemLista.objects.filter(user=user,treinodia__nome=self.dia).first()

                if not ordem_string:
                    ordem_string = OrdemLista.objects.filter(user=user,treinodiapadrao__nome=self.dia).first()
                if ordem_string:
                    ordem_Nova = organizar_list_ordem(qs,ordem_string.ordem)
                    qs  = sorted(qs,
                        key=lambda x: ordem_Nova.index(x) if x in ordem_Nova else len(ordem_Nova))
        else:
            qs=qs.filter(user=user,dia__nome=self.dia,video__categorias__categoria__icontains=categoria)
        if self.dia is None:
            return redirect('listas')    
        return qs
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        get = super().get_context_data(**kwargs)
        get['dia'] = self.dia

        treino_dia_page = TreinoDiaPadrao.objects.filter(user=self.user,dia__nome=self.dia)

        lista_dia_page = []
        for categoria in treino_dia_page:
            categorias = categoria.video.categorias.all()
            for nomes in categorias:
                nomes_categoria = str(nomes.categoria)
                lista_dia_page.append(nomes_categoria)
        categorias = set(lista_dia_page)
        get['categorias'] = categorias
        return get
    
    def get(self,*args,**kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        get = super().get(*args,**kwargs)

        return get
    
    def post(self,*args,**kwargs):
        if  not self.request.user.is_authenticated:
            return JsonResponse({'erro': 'Formato JSON inválido'}, status=200)
        dados_em_bytes = self.request.body

        try:
            dados_em_string = dados_em_bytes.decode('utf-8')

            dados_dict = json.loads(dados_em_string)
            dia = verificarString_numeros(dados_dict.get('dia'))
            if isinstance(dados_dict.get('id'),list):
                valores = dados_dict['id']
                if validacao_lista(valores):
                    lista = OrdemLista.objects.filter(treinodia__nome__icontains=dados_dict['dia'],user=self.request.user).first()
                    if not lista:
                        treinodia = UserDiasLista.objects.filter(nome=dados_dict['dia'],user=self.request.user).first()
                        if treinodia:
                            OrdemLista.objects.create(
                                ordem = valores,
                                treinodia= treinodia,
                                user= self.request.user,
                            )
                        else:
                            lista = OrdemLista.objects.filter(treinodiapadrao__nome__icontains=dados_dict['dia'],user=self.request.user).first()
                            if not lista:
                                treinodia = Dias.objects.filter(nome=dados_dict['dia']).first()
                                OrdemLista.objects.create(
                                    ordem = valores,
                                    treinodiapadrao = treinodia,
                                    user= self.request.user,
                                )
                            else:                        
                                lista.ordem = valores
                                lista.save()
                    else:
                        lista.ordem = valores
                        lista.save()
            else:
                if dados_dict.get('id').isnumeric() and dia == True:
                    user = self.request.user
                    dia = dados_dict['dia']
                    video_id = dados_dict['id']
                    treino = TreinoDiaPadrao.objects.filter(dia__nome=dia,user=user,video__id=video_id).first()
                    if not treino:
                        treino = TreinoDiaUser.objects.filter(dia__nome=dia,user=user,video__id=video_id).first()
                    treino.delete()
                    
            return JsonResponse({'mensagem': 'Dados recebidos com sucesso'})

        except json.JSONDecodeError as e:
            return JsonResponse({'erro': 'Formato JSON inválido'}, status=400)
    
class TreinoView(LoginRequiredMixin,CustomContextMixin,ListView):
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
        self.categoria = self.kwargs.get('categoria')

        self.treino_user_dia_lista = []

        treino_user_dia = TreinoDiaUser.objects.filter(user=self.request.user,dia__nome=self.dia)
        if not treino_user_dia:
            treino_user_dia = TreinoDiaPadrao.objects.filter(user=self.request.user,dia__nome=self.dia)

        self.user_lista = UserDiasLista.objects.filter(user=self.request.user)

        for id_video in treino_user_dia:
            self.treino_user_dia_lista.append(id_video.video.id)
        return setup

    def get_queryset(self):
        qs = super().get_queryset()

        filtro = bool(self.user_lista.filter(nome__icontains=self.categoria))
        
        if not self.categoria in ['Segunda','Terça','Quarta','Quinta','sexta'] and not filtro:
            categoria__url = self.categoria
            qs = qs.filter(categorias__categoria__icontains=categoria__url)
        return qs
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        get_contexto = super().get_context_data(**kwargs)
        get_contexto['categorias'] = CategoriaModel.objects.all()
        get_contexto['dia'] = self.dia

        get_contexto['lista_video_id'] = self.treino_user_dia_lista
        get_contexto['lista_treino'] = True

        return get_contexto
    
    def post(self,request,*args,**kwargs):
        selecionador = self.request.POST.getlist('videos')

        query_dia = Dias.objects.filter(nome=self.dia).first()
        if not query_dia:
            query_dia = UserDiasLista.objects.filter(nome=self.dia).first()

        categoria = self.categoria
        pagina_1 = self.request.POST.get('pagina_1')
        pagina_2 = self.request.POST.get('pagina_2')
        pagina_final = self.request.POST.get('pagina_final')
        pagina_4 = self.request.POST.get('pagina_4')

        lista_page = self.request.POST.getlist('id_page')

        if len(selecionador) >=1 :
            for id_video in selecionador:
                if len(self.treino_user_dia_lista) >= 1:
                    if len(lista_page)>=1:
                        lista_page.remove(str(id_video))
                if not int(id_video) in self.treino_user_dia_lista:
                    video = Videos.objects.get(id=id_video)
                    if query_dia._meta.model_name == 'userdiaslista':
                        TreinoDiaUser.objects.create(
                            dia=query_dia,
                            user=self.request.user,
                            video=video
                        )
                    else:
                        TreinoDiaPadrao.objects.create(
                            dia=query_dia,
                            user= self.request.user,
                            video=video
                        )
        if len(lista_page) >=1: 
            for id_video in lista_page:
                if int(id_video) in self.treino_user_dia_lista: 
                    if query_dia._meta.model_name == 'userdiaslista':
                        query_treino = TreinoDiaUser.objects.get(user=self.request.user,dia__nome=self.dia,video__id=int(id_video))
                    else:
                        query_treino= TreinoDiaPadrao.objects.get(user=self.request.user,dia__nome=self.dia,video__id=int(id_video))
                    query_treino.delete()

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
                return redirect(request.META.get('HTTP_REFERER', '/'))
            else:
                url = reverse('lista_treino',kwargs={'dia':self.dia,'categoria':cat})
                return redirect(url)
                
        url = reverse('lista_treino',kwargs={'dia':self.dia,'categoria':categoria}) + f'?page={pagina}'
        return redirect(url)
    

    
class TodosVideosView(CustomContextMixin,ListView):
    model = Videos
    context_object_name = 'videos'
    template_name = 'videos.html'
    paginate_by = 50
    ordering = ('-id')

    def get_queryset(self):
        qs = super().get_queryset()
        categoria = self.kwargs.get('categorias')
        if categoria == 'Geral':
            return qs
        if not categoria in ['Segunda','Terça','Quarta','Quinta','sexta']:
            categoria__url = categoria
            qs = qs.filter(categorias__categoria__icontains=categoria__url)
            return qs
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        get = super().get_context_data(**kwargs)
        get['dia'] = False
        get['categorias'] = CategoriaModel.objects.all()
        return get


class VideosZumba(CustomContextMixin,ListView):
    model = Videos
    context_object_name = 'videos'
    template_name = 'videos.html'
    paginate_by = 50
    ordering = ('-id')

    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset()
        qs = qs.filter(categorias__categoria='Zumba')
        return qs 
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        get = super().get_context_data(**kwargs)
        get['dia'] = False
        get['zumba'] = True
        return get
