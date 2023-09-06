from typing import Any, Dict
from django import http
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render,redirect,reverse
from django.views import View
from django.views.generic import ListView
from .models import Videos,TreinoDia,Dias,CategoriaModel
from django.contrib.auth.models import User
from time import sleep


class CustomContextMixin(ListView):
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        get = super().get_context_data(**kwargs)
        get['geral'] = 'Geral'
        return get

class HomePageView(CustomContextMixin,ListView):
    template_name = 'index.html'
    model = Dias
    context_object_name = 'dia_semana_index'

class ExercicioSemanaView(CustomContextMixin,ListView):
    model = TreinoDia
    template_name = 'dashboard.html'
    context_object_name = 'dia_semana'
    # paginate_by = 4
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
            qs = qs.filter(user=user,dia__nome=self.dia).order_by('id')
        else:
            qs=qs.filter(user=user,dia__nome=self.dia,video__categorias__categoria__icontains=categoria)
        if self.dia is None:
            return redirect('home')    
        return qs
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        get = super().get_context_data(**kwargs)
        get['dia'] = self.dia

        treino_dia_page = TreinoDia.objects.filter(user=self.user,dia__nome=self.dia)

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
    
class TreinoView(CustomContextMixin,ListView):
    model = Videos
    template_name = 'criartreino.html'
    context_object_name = 'videos'
    paginate_by = 4
    ordering = ('id')

    def setup(self,*args,**kwargs):
        setup = super().setup(*args,**kwargs)
        self.dia = self.kwargs.get('dia')
        self.categoria = self.kwargs.get('categoria')

        self.treino_user_dia_lista = []
        treino_user_dia = TreinoDia.objects.all().filter(user=self.request.user,dia__nome=self.dia)

        for id_video in treino_user_dia:
            self.treino_user_dia_lista.append(id_video.video.id)

        return setup

    def get_queryset(self):
        qs = super().get_queryset()
        
        if not self.categoria in ['Segunda','Terça','Quarta','Quinta','sexta']:
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
        query_dia = Dias.objects.get(nome=self.dia)
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
                    TreinoDia.objects.create(
                        dia=query_dia,
                        user= self.request.user,
                        video=video
                    )
        if len(lista_page) >=1: 
            for id_video in lista_page:
                if int(id_video) in self.treino_user_dia_lista: 
                    query_treino= TreinoDia.objects.get(user=self.request.user,dia__nome=self.dia,video__id=int(id_video))
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
                url = reverse('lista_treino',kwargs={'dia':query_dia.nome,'categoria':self.dia})
                return redirect(url)
            if cat is None:
                return redirect(request.META.get('HTTP_REFERER', '/'))
            else:
                url = reverse('lista_treino',kwargs={'dia':query_dia.nome,'categoria':cat})
                return redirect(url)
                
        url = reverse('lista_treino',kwargs={'dia':query_dia.nome,'categoria':categoria}) + f'?page={pagina}'
        return redirect(url)
    
    def get(self,*args,**kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        dia = self.dia
        if not dia in ['Segunda','Terça','Quarta','Quinta','sexta']:
                return redirect('dia')
        get = super().get(*args,**kwargs)
        return get    

class DiaCriarView(CustomContextMixin,ListView):
    model = Dias
    template_name = 'diatreinocriar.html'
    context_object_name = 'dias'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        get = super().get_context_data(**kwargs)
        get['lista_treino'] = True
        return get
    
    def get(self,*args,**kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        get = super().get(*args,**kwargs)

        return get    
    
class TodosVideosView(CustomContextMixin,ListView):
    model = Videos
    context_object_name = 'videos'
    template_name = 'videos.html'
    paginate_by = 5
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
    paginate_by = 5
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
