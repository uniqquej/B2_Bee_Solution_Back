import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'beesolution.settings')
django.setup()

import numpy as np
from PIL import Image
from PIL import ImageDraw, ImageFont
from article.models import Solution

def make_wise_image(idx):
    # 요청 정보 가져오기
    target = Solution.objects.get(id=idx)
    image_url = target.solution_image
    img = Image.open(f'media/{image_url}').convert('RGB')
    img = img.resize((600,400))
    draw = ImageDraw.Draw(img, 'RGBA')
    
    # 명언 정보 가져오기
    input_wise = target.wise
    wise_len = len(input_wise)
    
    
    # 글자수에따라 폰트 / 폰트크기에 따라 줄간격 조정
    if wise_len <= 40:
        fontsize = 40
        y_upper = 45
    else:
        fontsize = 30
        y_upper = 35
    
    # 개행 수에 따라 y축 정렬
    text = input_wise.split('/')
    if fontsize == 40:
        y = 200 - (len(text) * 25)
    elif fontsize == 30:
        y = 200 - (len(text) * 17)
    
    font = ImageFont.truetype("fonts/NotoSerifKR-Bold.otf", fontsize)
    
    # 텍스트 삽입
    for i in text:
        # 텍스트 수에 따라 x축 중앙 정렬
        space = i.count(" ")
        if fontsize == 40:
            x = 300 - (len(i) * 20) + (space * 16)
        elif fontsize == 30: 
            x = 300 - (len(i) * 13) + (space * 8)
            
        position = (x, y)
        left, top, right, bottom = draw.textbbox(position, i, font=font)
        draw.rectangle((left-2, top-2, right+2, bottom+2), fill=(0,0,0,150))
        draw.text(position, i, font=font, fill=(255,255,255))
        y+=y_upper
        
    # nickname 삽입
    if target.nickname:
        input_nickname = " - " + target.nickname
        x = 400 - (len(input_nickname) * 5)
        y += 30
        position = (x, y)
        
        fontsize = 15
        font_nickname = ImageFont.truetype("fonts/NotoSerifKR-Bold.otf", fontsize)
        left, top, right, bottom = draw.textbbox(position, input_nickname, font=font_nickname)
        draw.rectangle((left-5, top-5, right+5, bottom+5), fill=(0,0,0,150))
        draw.text(position, input_nickname, font=font_nickname, fill=(255,255,255))
    
    img.save(f'./media/{image_url}', 'jpeg')