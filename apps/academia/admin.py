from django.contrib import admin
from .models import Dias,Videos,TreinoDia

class DiasAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    ordering =('id',)


class VideosAdmin(admin.ModelAdmin):
    list_display = ('exercicio','time')
    ordering =('id',)
    
class TreinoDiaAdmin(admin.ModelAdmin):
    list_display = ('dia','video','user')


admin.site.register(Videos,VideosAdmin)
admin.site.register(Dias,DiasAdmin)
admin.site.register(TreinoDia,TreinoDiaAdmin)


