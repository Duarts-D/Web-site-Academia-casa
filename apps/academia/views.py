from typing import Any, Dict
from django.db.models.query import QuerySet
from django.shortcuts import render,redirect,reverse
from django.views import View
from django.views.generic import ListView
from .models import Videos,TreinoDia,Dias,CategoriaModel
from django.contrib.auth.models import User
from time import sleep

def lista_ids_video(lista=[]):
    return lista


class HomePageView(ListView):
    template_name = 'index.html'
    model = Dias
    context_object_name = 'dia_semana_index'
    

class ExercicioSemanaView(ListView):
    model = TreinoDia
    template_name = 'dashboard.html'
    context_object_name = 'dia_semana'
    paginate_by = 4
    ordering = ('-id')

    def get_queryset(self):
        qs = super().get_queryset()
        dia = self.kwargs.get('dia')
        user = self.request.user
        
        qs = qs.filter(user=user,dia__nome=dia).order_by('id')
        
        if dia is None:
            return redirect('home')    
        return qs
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        get = super().get_context_data(**kwargs)
        dia = self.kwargs.get('dia')
        get['dia'] = dia

        return get
    
    def get(self,*args,**kwargs):
        if not self.request.user.is_authenticated:
            return redirect('login')
        get = super().get(*args,**kwargs)

        return get
    
class TreinoView(ListView):
    model = Videos
    template_name = 'criartreino.html'
    context_object_name = 'videos'
    paginate_by = 4
    ordering = ('id')

    def setup(self,*args,**kwargs):
        super().setup(*args,**kwargs)
        self.dia = self.kwargs.get('dia')
        self.dd = self.kwargs.get('dd')
        self.lista_video_id = []
        if not self.request.user.is_authenticated:
            return redirect('login')
        treino_user_dia = TreinoDia.objects.all().filter(user=self.request.user,dia__nome=self.dia)

        for id_video in treino_user_dia :
            self.lista_video_id.append(id_video.video.id)

    def get_queryset(self):
        qs = super().get_queryset()
        categoria = self.kwargs.get('categoria',None)
        if categoria == 'Nenhum':
            return qs
        if not categoria in ['Segunda','Terça','Quarta','Quinta','sexta']:
            categoria__url = self.kwargs.get('categoria',None)
            qs = qs.filter(categorias__categoria=categoria__url)
        return qs
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        get = super().get_context_data(**kwargs)
        page = get['page_obj']
        get['categorias'] = CategoriaModel.objects.all()
        lista_ids_videos = lista_ids_video()
        for video in page:
            lista_ids_videos.append(video.id)
        try:
            get['dia'] = self.dia
            get['lista_video_id'] = self.lista_video_id
            get['lista_treino'] = True
        except AttributeError:
            get['dia'] = None
        return get
    
    def post(self,request,*args,**kwargs):
        selecionador = self.request.POST.getlist('videos')
        query_dia = Dias.objects.get(nome=self.dia)
        categoria = self.kwargs.get('categoria')
        pagina_1 = self.request.POST.get('pagina_1')
        pagina_2 = self.request.POST.get('pagina_2')
        a_lista = lista_ids_video()
        lista_limpa = list(set(a_lista))
        sleep(2)
        for id_video in selecionador:
            if len(lista_limpa) >= 1:
                lista_limpa.remove(int(id_video))
            if not int(id_video) in self.lista_video_id:
                video = Videos.objects.get(id=id_video)
                TreinoDia.objects.create(
                    dia=query_dia,
                    user= self.request.user,
                    video=video
                )
        
        for id_video in lista_limpa:
            if int(id_video) in self.lista_video_id:
                query_treino= TreinoDia.objects.get(user=self.request.user,dia__nome=self.dia,video__id=id_video)
                query_treino.delete()
        a_lista = lista_ids_video().clear()

        if not pagina_1 is None:
            pagina_1 = int(pagina_1)-1
            pagina = pagina_1
        elif not pagina_2 is None:
            pagina_2 = int(pagina_2)+1
            pagina = pagina_2
        else:
            return redirect('home')
                
        url = reverse('lista_treino',kwargs={'dia':query_dia.nome,'categoria':categoria}) + f'?page={pagina}'
        return redirect(url)
    
    def get(self,*args,**kwargs):
        lista_ids_video().clear()
        if not self.request.user.is_authenticated:
            return redirect('login')
        if self.dia is None:
            return redirect('dia')
        get = super().get(*args,**kwargs)
        return get    

class DiaCriarView(ListView):
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
    
class TodosVideosView(ListView):
    model = Videos
    context_object_name = 'videos'
    template_name = 'videos.html'
    paginate_by = 5
    ordering = ('-id')

class VideosZumba(ListView):
    model = Videos
    context_object_name = 'videos'
    template_name = 'videos.html'
    paginate_by = 5
    ordering = ('-id')

    def get_queryset(self) -> QuerySet[Any]:
        qs = super().get_queryset()
        qs = qs.filter(categorias__categoria='ZUMBA')
        return qs 