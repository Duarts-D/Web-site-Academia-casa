from PIL import Image, ImageDraw , ImageFont
import os
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO


def img_text(imagem):
    if not imagem:
        return

    img = Image.open(imagem)
    draw = ImageDraw.Draw(img)
    font = 'apps/academia/font/PlayfairDisplay-ExtraBoldItalic.ttf'
    x , y = img.size
    size_text = 24
    if x <= 400 :
        size_text = 12

    fonte = ImageFont.truetype(font,size=size_text)

    posicao_x = x - (x * ( 90 / 100) )
    posicao_y = y - (y * ( 5 / 100))

    texto = 'ACADEMIA EM QUALQUER LUGAR'
    draw.text((posicao_x,posicao_y), text=texto ,font=fonte,fill='black')
    buffer = BytesIO()
    img.save(buffer,format='PNG')

    img_new = InMemoryUploadedFile(
            buffer, None, f"{imagem.name.split('/')[-1].split('.')[0]}.jpeg",
            'image/jpeg', buffer.tell(), None)
    return img_new