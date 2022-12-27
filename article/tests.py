from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User
from article.models import Rating

# 이미지 업로드
from django.test.client import MULTIPART_CONTENT, encode_multipart, BOUNDARY
from PIL import Image
import tempfile

def get_temporary_image(temp_file):
    size = (500, 500)
    color = (255, 0, 0, 0)
    image = Image.new("RGBA", size, color)
    image.save(temp_file, 'png')
    return temp_file

class ArticleCreateTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_data = {'username':'john', 'password':'password1!'}
        cls.worry_data = {'my_id': 114, 'category' : '일상', 'solution':99, 'content':'some content', 'mbti':'ESFJ'}
        cls.user = User.objects.create_user('john', 'password1!')
    
    def setUp(self):
        self.access_token = self.client.post(reverse('user_auth_view'), self.user_data).data['access']
    
    def test_fail_if_not_logged_in(self):
        url = reverse("make_worry")
        reponse = self.client.get(url)
        self.assertEqual(reponse.status_code, 401)
    
    # def test_created_worry(self):
    #     reponse = self.client.post(
    #         path=reverse("make_worry"),
    #         data=self.worry_data,
    #         HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
    #     )
    #     self.assertEqual(reponse.status_code, 200)
    
    # def test_make_solution(self):
    #     temp_file = tempfile.NamedTemporaryFile()
    #     temp_file.name = "image.png"
    #     image_file = get_temporary_image(temp_file)
    #     image_file.seek(0)
    #     self.make_solution_data = {'solution_image':image_file, 'wise':'abcdefg', 'article_id':2 }
    #     response = self.client.post(
    #         path = reverse("make_solution"),
    #         data = encode_multipart(data = self.make_solution_data, boundary=BOUNDARY),
    #         content_type=MULTIPART_CONTENT,
    #         HTTP_AUTHORIZATION= f"Bearer {self.access_token}"
    #     )
    #     self.assertEqual(response.status_code, 200)
