from django.urls import reverse
from rest_framework.test import APITestCase
from users.models import User, UserChr
from article.models import Rating, Category, Solution, Article
from faker import Faker
import random

class MakeWorryTest(APITestCase):
    """
    고민 작성하기 테스트
    """
    @classmethod
    def setUpTestData(cls):
        cls.faker = Faker()
        mbti_list = ['ENFP', 'ENFJ', 'ENTP', 'ENTJ', 'ESFP', 'ESFJ', 'ESTP', 'ESTJ',
                        'INFP', 'INFJ', 'INTP', 'INTJ', 'ISFP', 'ISFJ', 'ISTP', 'ISTJ']
        
        for i in range(1,101):
            cls.user = User.objects.create_user(
                username = cls.faker.name(),
                password = 'xptmxm123!'
            )
            
            cls.user_chr = UserChr.objects.create(
                user_id = i,
                mbti = random.choice(mbti_list),
                gender = random.choice(['W','M']),
                age = random.randrange(10,80)
            )
        cls.user_id = 1    
        cls.user_data = {'username':User.objects.get(id = cls.user_id), 'password':'xptmxm123!'}
        
        category_list = ['일상', '취미', '취업', '음식']
        for cate in category_list:
            cls.category = Category.objects.create(category = cate)
            
            for _ in range(10):
                cls.solution = cls.category.connected_solution.create(
                    user_id = random.randrange(1, 100),
                    wise = cls.faker.sentence()
                )
                
        for _ in range(100):
            cls.rating = Rating.objects.create(
                user_id = random.randrange(1,100),
                solution_id = random.randrange(1,40),
                rating = random.choice([0,2,4])
            )
            
    def setUp(self): # 매 테스트마다 실행
       self.access_token = self.client.post(reverse('user_auth_view'), self.user_data).data['access']
    
    def test_make_worry(self):
        url = reverse('make_worry')
        category = random.choice(['일상', '취미', '취업', '음식'])
        response = self.client.post(
            path = url,
            data = {'category':category,
                    'content': self.faker.sentence(),
                    'mbti':UserChr.objects.get(user_id=self.user_id).mbti
                    },
            HTTP_AUTHORIZATION = f'Bearer {self.access_token}'
        )
        # print('makeworry_post : ' ,response.data)
        self.assertEqual(response.status_code, 200)

class LoadArticleTest(APITestCase):
    """
    사용자가 작성한 고민 중 가장 최신 고민 한가지 읽어오기 테스트
    """
    @classmethod
    def setUpTestData(cls):
        cls.faker = Faker()
        mbti_list = ['ENFP', 'ENFJ', 'ENTP', 'ENTJ', 'ESFP', 'ESFJ', 'ESTP', 'ESTJ',
                        'INFP', 'INFJ', 'INTP', 'INTJ', 'ISFP', 'ISFJ', 'ISTP', 'ISTJ']
        
        for i in range(1,101):
            cls.user = User.objects.create_user(
                username = cls.faker.name(),
                password = 'xptmxm123!'
            )
            
            cls.user_chr = UserChr.objects.create(
                user_id = i,
                mbti = random.choice(mbti_list),
                gender = random.choice(['W','M']),
                age = random.randrange(10,80)
            )
        cls.user_id = 1    
        cls.user_data = {'username':User.objects.get(id = cls.user_id), 'password':'xptmxm123!'}
        
        category_list = ['일상', '취미', '취업', '음식']
        for cate in category_list:
            cls.category = Category.objects.create(category = cate)
            
            for _ in range(10):
                cls.solution = cls.category.connected_solution.create(
                    user_id = random.randrange(1, 100),
                    wise = cls.faker.sentence()
                )
                
            for _ in range(100):
                cls.rating = Rating.objects.create(
                user_id = random.randrange(1,100),
                solution_id = random.randrange(1,40),
                rating = random.choice([0,2,4])
            )
                
        for _ in range(3):
            cls.article_solution = Solution.objects.get(id = random.randrange(1,40))
            cls.article = cls.article_solution.connected_article.create(
                user_id = cls.user_id,
                category = random.choice(category_list),
                content = cls.faker.sentence(),
                mbti = UserChr.objects.get(user_id = cls.user_id).mbti                
            )
    
    def setUp(self):
        self.access_token = self.client.post(reverse('user_auth_view'), self.user_data).data['access']
    
    def test_get_make_worry(self):
        url = reverse('make_worry')
        response = self.client.get(
            path = url,
            HTTP_AUTHORIZATION = f'Bearer {self.access_token}'
        )
        # print('make_worry_get : ', response.data)
        self.assertEqual(response.status_code,200)

class DetailArticleTest(APITestCase):
    '''
    고민 수정, 삭제 테스트
    '''
    @classmethod
    def setUpTestData(cls):
        cls.faker = Faker()
        cls.user_data = {'username':'test1','password':'xptmxm123!'}
        cls.user = User.objects.create_user(
            username = 'test1',
            password = 'xptmxm123!'
        )
        for _ in range(5):
            cls.article = Article.objects.create(
                user_id = 1,
                content =  cls.faker.sentence(),
                mbti = 'ISFJ',
                category = '일상'
            )
        
        cls.current_article = Article.objects.get(id=1)
    
    def setUp(self):
         self.access_token = self.client.post(reverse('user_auth_view'), self.user_data).data['access']
    
    def test_edit_article(self):
        url = reverse('detail_article', args=[self.current_article.pk])
        response = self.client.put(
            path = url,
            data = {
                "content" : "edit!!",
                "category": "취업"
                },
            HTTP_AUTHORIZATION = f'Bearer {self.access_token}'
        )
        print(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['content'], "edit!!")
    
    def test_delete_article(self):
        url = reverse('detail_article', args=[self.current_article.pk])
        response = self.client.delete(
            path = url,
            HTTP_AUTHORIZATION = f'Bearer {self.access_token}'
        )
        print(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Article.objects.count(), 4)
        

class MainViewTest(APITestCase):
    '''
    article 카테고리 별 조회
    '''
    @classmethod
    def setUpTestData(cls):
        cls.faker = Faker()
        cls.user_data = {'username' : 'test1', 'password' : 'xptmxm123!'}
        cls.user = User.objects.create_user('test1','xptmxm123!')
        
        cls.category_list = ['일상', '취미', '취업', '음식']
        for category in cls.category_list:
            cls.article = Article.objects.create(
                user_id = 1,
                content = cls.faker.sentence(),
                mbti = 'ISFJ',
                category = category
            )
    
    def setUp(self):
        self.access_token = self.client.post(reverse('user_auth_view'), self.user_data).data['access']
        
    def test_load_main(self):
        self.category_id = 1
        url = reverse('main', args=[self.category_id])
        response = self.client.get(
            path = url,
            HTTP_AUTHORIZATION = f'Bearer {self.access_token}'
        )
        # print(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['results'][0]['category'], self.category_list[self.category_id-1])

class ProfileViewTest(APITestCase):
    '''
    프로필 페이지 article 카테고리 별 조회
    '''
    @classmethod
    def setUpTestData(cls):
        cls.faker = Faker()
        cls.user_data = {'username' : 'test2', 'password' : 'xptmxm123!'}
        cls.user = User.objects.create_user('test1','xptmxm123!')
        cls.user2 = User.objects.create_user('test2','xptmxm123!')
        
        cls.category_list = ['일상', '취미', '취업', '음식']
        for category in cls.category_list:
            cls.article = Article.objects.create(
                user_id = 1,
                content = cls.faker.sentence(),
                mbti = 'ISFJ',
                category = category
            )
            cls.article2 = Article.objects.create(
                user_id = 2,
                content = cls.faker.sentence(),
                mbti = 'ISFJ',
                category = category
            )
    
    def setUp(self):
        self.access_token = self.client.post(reverse('user_auth_view'), self.user_data).data['access']
        
    def test_load_profile(self):
        self.category_id = 1
        url = reverse('profile_article', args=[self.category_id])
        response = self.client.get(
            path = url,
            HTTP_AUTHORIZATION = f'Bearer {self.access_token}'
        )
        print(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['results'][0]['user'], self.user2.pk)
        self.assertEqual(response.data['results'][0]['category'], self.category_list[self.category_id-1])
        
    
class PromotionViewTest(APITestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.faker = Faker()
        mbti_list = ['ENFP', 'ENFJ', 'ENTP', 'ENTJ', 'ESFP', 'ESFJ', 'ESTP', 'ESTJ',
                        'INFP', 'INFJ', 'INTP', 'INTJ', 'ISFP', 'ISFJ', 'ISTP', 'ISTJ']
        
        for i in range(1,101):
            cls.user = User.objects.create_user(
                username = cls.faker.name(),
                password = 'xptmxm123!'
            )
            
            cls.user_chr = UserChr.objects.create(
                user_id = i,
                mbti = random.choice(mbti_list),
                gender = random.choice(['W','M']),
                age = random.randrange(10,80)
            )
        
        category_list = ['일상', '취미', '취업', '음식']
        for cate in category_list:
            cls.category = Category.objects.create(category = cate)
            
            for _ in range(10):
                cls.solution = cls.category.connected_solution.create(
                    user_id = random.randrange(1, 100),
                    wise = cls.faker.sentence()
                )
                
        for _ in range(100):
            cls.rating = Rating.objects.create(
                user_id = random.randrange(1,100),
                solution_id = random.randrange(1,40),
                rating = random.choice([0,2,4])
            )
    
    def test_promotion(self):
        url = reverse('make_worry_promotion')
        response = self.client.post(
            path = url,
            data = {
                "mbti" : "ISFP",
                "category" : "일상",
                "content" : "promotion testing"
            }
        )
        
        self.assertEqual(response.status_code, 200)