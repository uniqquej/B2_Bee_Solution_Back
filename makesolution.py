import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'beesolution.settings')
django.setup()

import numpy as np
from PIL import Image
from PIL import ImageDraw, ImageFont
from article.models import Solution

def make_wise_image(idx):
    target = Solution.objects.get(id=idx)
    image_url = target.solution_image
    img = Image.open(f'media/{image_url}').convert('RGB')
    img = img.resize((550,400))
    draw = ImageDraw.Draw(img)
    
    font = ImageFont.truetype("fonts/NotoSerifKR-Bold.otf", 30) # 폰트변경
    
    text = "첫번째줄입니다wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww"
    text2 = "두번째줄입니다"
    
    position = (50, 180)
    position2 = (50, 220)

    bbox = draw.textbbox(position, text, font=font)
    draw.rectangle(bbox, fill="white")
    bbox2 = draw.textbbox(position2, text, font=font)
    draw.rectangle(bbox2, fill="black")
    
    draw.text(position, text, font=font, fill=(0,0,0))
    draw.text(position2, text2, font=font, fill=(255,255,255))
    
    img.show()
    img.save(f'./media/{image_url}', 'jpeg')