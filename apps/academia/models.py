from django.db import models
from django.contrib.auth.models import User

    
class CategoriaModel(models.Model):
    categoria = models.CharField(max_length=100)

    def __str__(self):
        return self.categoria

class Dias(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome

class UserDiasLista(models.Model):
    nome = models.CharField(max_length=30)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.nome

class Videos(models.Model):
    exercicio = models.CharField(max_length=255)
    video = models.CharField(max_length=255)
    quantidade = models.PositiveIntegerField(default=0)
    time = models.PositiveIntegerField(default=0)
    repeticao = models.PositiveIntegerField(default=0)
    id_video_youtube = models.CharField(max_length=50,default=1)
    categorias = models.ManyToManyField(CategoriaModel)
    info = models.CharField(max_length=255,blank=False,null=True,default='...')
    imagem = models.ImageField(upload_to='media/',blank=True,null=True)
    id_video_youtube_didatico = models.CharField(max_length=50,default=1)

    def save(self,*args,**kwargs):
        if self.id_video_youtube == '1':
            self.id_video_youtube = self.video
        if len(self.video) <= 20:
            self.video = 'https://www.youtube.com/embed/' + self.video
        super().save(*args,**kwargs)

    def __str__(self):
        return self.exercicio
    

class TreinoDiaPadrao(models.Model):
    dia = models.ForeignKey(Dias,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    video = models.ForeignKey(Videos,on_delete=models.CASCADE)

    def __str__(self):
        return self.dia.nome


class TreinoDiaUser(models.Model):
    dia = models.ForeignKey(UserDiasLista,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    video = models.ForeignKey(Videos,on_delete=models.CASCADE)

    def __str__(self):
        return self.dia.nome

class OrdemLista(models.Model):
    ordem = models.CharField(max_length=255)
    treinodia = models.ForeignKey(UserDiasLista,on_delete=models.CASCADE,null=True, blank=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    treinodiapadrao = models.ForeignKey(Dias,on_delete=models.CASCADE,null=True, blank=True)

    def __str__(self) -> str:
        return self.ordem