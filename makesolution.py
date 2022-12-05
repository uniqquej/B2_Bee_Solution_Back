import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'beesolution.settings')
django.setup()

import cv2
import numpy as np
from PIL import Image
from PIL import ImageDraw, ImageFont
from article.models import Solution2

def makewisepicture(idx):
    target = Solution2.objects.get(id=idx)
    image_url = target.solution_image
    img = Image.open(f'media/{image_url}').convert('RGB')
    img = img.resize((550,400))
    draw = ImageDraw.Draw(img)
    
    font = ImageFont.truetype("fonts/NotoSerifKR-Bold.otf", 30)
    text = "첫번째줄입니다"
    text2 = "두번째줄입니다"
    draw.text((50, 180), text, font=font, fill=(0,0,0))
    draw.text((50, 220), text2, font=font, fill=(0,0,0))

    img.show()
    img.save(f'./media/{image_url}', 'jpeg')