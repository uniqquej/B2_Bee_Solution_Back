from rest_framework.test import APITestCase
from django.urls import reverse
from faker import Faker
from users.models import User, UserChr
from article.models import Article, Solution, Rating, Category
import random

#이미지 업로드
from django.test.client import MULTIPART_CONTENT, encode_multipart, BOUNDARY
from PIL import Image
import tempfile

def get_temporary_image(temp_file):
    size = (200,200)
    color = (255,0,0)
    image = Image.new('RGBA', size, color)
    image.save(temp_file,'png')
    return temp_file

class MakeSolutionViewTest(APITestCase):
    '''
    Solution 만들기 테스트
    '''
    @classmethod
    def setUpTestData(cls):
        cls.faker = Faker()
        cls.user_data = {'username' : 'test1', 'password':'xptmxm123!'}
        cls.user = User.objects.create_user('test1','xptmxm123!')
        cls.user_chr = UserChr.objects.create(mbti='ISFJ', age=22, gender='M', user_id = 1)
        cls.article = Article.objects.create(category='일상', content='first content', user = cls.user)
        
        category_list = ['일상', '취미', '취업', '음식']
        for cate in category_list:
            cls.category = Category.objects.create(category = cate)
    
    def setUp(self):
        self.access_token = self.client.post(reverse('user_auth_view'), self.user_data).data['access']
    
    def test_make_solution_no_article(self):
        url = reverse('make_solution', args=[0])
        temp_file = tempfile.NamedTemporaryFile()
        temp_file.name = 'solution.png'
        image_file = get_temporary_image(temp_file)
        image_file.seek(0)
        
        response = self.client.post(
            path = url,
            data = {
                'solution_image' : image_file,
                'wise' : self.faker.sentence(),
                'category' : 1
            },
            HTTP_AUTHORIZATION = f'Bearer {self.access_token}'
        )
        self.assertEqual(response.status_code, 200)
    
    def test_make_solution_article(self):
        url = reverse('make_solution', args=[self.article.id])
        temp_file = tempfile.NamedTemporaryFile()
        temp_file.name = 'solution.png'
        image_file = get_temporary_image(temp_file)
        image_file.seek(0)
        
        response = self.client.post(
            path = url,
            data = encode_multipart(data = {
                'solution_image' : image_file,
                'wise' : self.faker.sentence(),
                'category' : 2
            }, boundary = BOUNDARY),
            content_type=MULTIPART_CONTENT,
            HTTP_AUTHORIZATION = f'Bearer {self.access_token}'
        )

        print(Solution.objects.get(id=1).category) #none이 나옴
        print(Article.objects.get(id=self.article.id).solution) #none이 나옴
        self.assertEqual(response.status_code, 200)

class LoadSolutionTest(APITestCase):
    '''
    article 별 solution 조회 테스트
    '''
    @classmethod
    def setUpTestData(cls):
        cls.faker = Faker()
        for _ in range(10):
            cls_user = User.objects.create_user(
                username = cls.faker.name(),
                password = 'xptmxm123!'
            )
        cls.currrent_user = User.objects.create_user('test1','xptmxm123!')
        cls.user_data = {'username' : 'test1', 'password':'xptmxm123!'}
        cls.user_chr = UserChr.objects.create(mbti='ISFJ', age=22, gender='M', user_id = 1)
        
        category_list = ['일상', '취미', '취업', '음식']
        for cate in category_list:
            cls.category = Category.objects.create(category = cate)
        
        cls.article = Article.objects.create(category='일상', content='first content', user = cls.currrent_user)
        for _ in range(5):
            cls.article.solution.create(
                wise = cls.faker.sentence(),
                user_id = random.randrange(1, 10)
            )
    
    def test_get_solution(self):
        url = reverse('make_solution', args=[self.article.id])
        response = self.client.get(url)
        
        print(response.data)
        print(Solution.objects.get(id = 1).connected_article) #none
        self.assertEqual(response.status_code, 200)

class LoadAllSolutionTest(APITestCase):
    '''
    모든 솔루션 조회
    '''
    @classmethod
    def setUpTestData(cls):
        cls.faker = Faker()
        cls.user = User.objects.create_user('test1','xptmxm123!')
        cls.user2 = User.objects.create_user('test2','xptmxm123!')
        
        category_list = ['일상', '취미', '취업', '음식']
        for cate in category_list:
            cls.category = Category.objects.create(category = cate)
            
            cls.solution = cls.category.connected_solution.create(
                user_id = cls.user.pk,
                wise = cls.faker.sentence()
            )
            
            cls.solution2 = cls.category.connected_solution.create(
                user_id = cls.user2.pk,
                wise = cls.faker.sentence()
            )
        
    def setUp(self):
        self.access_token = self.client.post(reverse('user_auth_view'), {'username':'test2','password':'xptmxm123!'}).data['access']
                
    def test_load_all_solution(self):
        url = reverse('all_solution')
        response = self.client.get(
            path = url
        )
        print(response.data)
        self.assertEqual(response.status_code,200)
        self.assertEqual(Solution.objects.count(), 8)
    
    def test_load_my_solution(self):
        url = reverse('my_solution')
        response = self.client.get(
            path = url,
            HTTP_AUTHORIZATION = f'Bearer {self.access_token}'
        )
        # print(response.data)
        
        for i in response.data:
            self.assertEqual(i['user'],2)
            
        self.assertEqual(response.status_code,200)
        
        