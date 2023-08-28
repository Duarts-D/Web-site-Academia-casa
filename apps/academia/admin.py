from django.contrib import admin
from .models import Dias,Videos,TreinoDia,CategoriaModel

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


admin.site.register(Videos,VideosAdmin)
admin.site.register(Dias,DiasAdmin)
admin.site.register(TreinoDia,TreinoDiaAdmin)
admin.site.register(CategoriaModel,CategoriaAdmin)


