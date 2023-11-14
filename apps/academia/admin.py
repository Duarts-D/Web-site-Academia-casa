from django.contrib import admin
from .models import Dias,Videos,TreinoDiaPadrao,CategoriaModel,OrdemLista,EquipamentoModel

class DiasAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    ordering =('id',)


class VideosAdmin(admin.ModelAdmin):
    list_display = ('exercicio','time')
    ordering =('id',)
    search_fields = ('exercicio',)
    
class TreinoDiaAdmin(admin.ModelAdmin):
    list_display = ('dia','video','user')


class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('categoria',)

class OrdermListaAdmin(admin.ModelAdmin):
    list_display = ('treinodiapadrao','user')

class EquipamentoAdmin(admin.ModelAdmin):
    list_display = ('equipamento',)

admin.site.register(Videos,VideosAdmin)
admin.site.register(Dias,DiasAdmin)
admin.site.register(TreinoDiaPadrao,TreinoDiaAdmin)
admin.site.register(CategoriaModel,CategoriaAdmin)
admin.site.register(OrdemLista,OrdermListaAdmin)
admin.site.register(EquipamentoModel,EquipamentoAdmin)