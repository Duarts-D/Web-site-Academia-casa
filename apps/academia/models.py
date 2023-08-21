from django.db import models
from django.contrib.auth.models import User


CATEGORIAS = (
    ("ABDOMEN","ABDOMEN"),
    ("BRACOS","BRAÇOS"),
    ("GLÚTEOS","GLÚTEOS"),
    ("PERNAS","PERNAS"),
    ("PEITO","PEITO"),
    ("TRICEPS","TRICEPS"),
    ("ZUMBA","ZUMBA"),
    ("1","NENHUM"),
)

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
    categorias = models.CharField(max_length=15,choices=CATEGORIAS,default="1")

    def save(self,*args,**kwargs):
        if self.id_video_youtube == '1':
            self.id_video_youtube = self.video
        if len(self.video) <= 20:
            self.video = 'https://www.youtube.com/embed/' + self.video
        super().save(*args,**kwargs)

    def __str__(self):
        return self.exercicio
    

class TreinoDia(models.Model):
    dia = models.ForeignKey(Dias,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    video = models.ForeignKey(Videos,on_delete=models.CASCADE)

    def __str__(self):
        return self.dia.nome
