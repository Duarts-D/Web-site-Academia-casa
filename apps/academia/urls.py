from django.urls import path
from .views import HomePageView,ListasView,ExercicioSemanaView,TreinoView,TodosVideosView,VideosZumba

urlpatterns = [
    path('', HomePageView.as_view(), name="home"),
    path('Listas/',ListasView.as_view(),name='listas'),
    path('Treino-dia-<str:dia>/<str:categoria>',ExercicioSemanaView.as_view(),name='exercicios'),
    path('Adicionar-Treino/<str:dia>-<str:categoria>',TreinoView.as_view(),name='lista_treino'),
    path('Videos-<str:categorias>/',TodosVideosView.as_view(),name='videos'),
    path('Videos-Zumba',VideosZumba.as_view(),name='videos_zumba'),
]
