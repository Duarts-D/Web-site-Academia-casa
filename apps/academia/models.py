from django.db import models
from django.contrib.auth.models import User
import re

class Dias(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome
    
class Videos(models.Model):
    exercicio = models.CharField(max_length=255)
    video = models.CharField(max_length=255)
    quantidade = models.PositiveIntegerField(default=0)
    time = models.PositiveIntegerField(default=0)
    repeticao = models.PositiveIntegerField(default=0)
    id_video_youtube = models.CharField(max_length=50,default=1)

    def save(self,*args,**kwargs):
        if self.id_video_youtube == '1':
            regex = r"embed/([a-zA-Z0-9_-]+)"
            match = re.search(regex, self.video)
            self.id_video_youtube = match.group(1)
            super().save(*args,**kwargs)
        
    
    def __str__(self):
        return self.exercicio
    

class TreinoDia(models.Model):
    dia = models.ForeignKey(Dias,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    video = models.ForeignKey(Videos,on_delete=models.CASCADE)

    def __str__(self):
        return self.dia.nome
