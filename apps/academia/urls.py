from django.urls import path
from .views import HomePageView,ExercicioSemanaView,TreinoView,DiaCriarView,TodosVideosView,VideosZumba

urlpatterns = [
    path('',HomePageView.as_view(),name='home'),
    path('<str:dia>',ExercicioSemanaView.as_view(),name='exercicios'),
    path('criar_treino/<str:dia>/<str:categoria>',TreinoView.as_view(),name='lista_treino'),
    path('dia/',DiaCriarView.as_view(),name='dia'),
    path('videos/',TodosVideosView.as_view(),name='videos'),
    path('videos/zumba',VideosZumba.as_view(),name='videos_zumba'),
]
