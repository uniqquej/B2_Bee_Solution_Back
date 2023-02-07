from django.urls import reverse
from rest_framework.test import APITestCase
from users.models import User, UserChr
from article.models import Article,Comment
from faker import Faker
from article.serializers import CommentSerializer
import random

class CommentCreateTest(APITestCase):
    """
    댓글 생성 테스트
    """
    @classmethod
    def setUpTestData(cls): # 최초 한 번만 실행 > 데이터가 많아질수록 효율적
        cls.user_data = {'username' : 'test1', 'password':'xptmxm123!'}
        cls.user = User.objects.create_user('test1','xptmxm123!')
        cls.user_chr = UserChr.objects.create(mbti='ISFJ', age=22, gender='M', user_id = 1)
        cls.article = Article.objects.create(category='일상', content='first content',user = cls.user)
    
    def setUp(self): # 매 테스트마다 실행
       self.access_token = self.client.post(reverse('user_auth_view'), self.user_data).data['access']
    
    def test_create_comment(self):
        url = reverse('comment_view', args=[self.article.id])
        response = self.client.post(
            path = url, 
            data = {'content':"1등이야"},
            HTTP_AUTHORIZATION = f"Bearer {self.access_token}")
        print(response.data)
        self.assertEqual(response.status_code, 201)

class LoadCommentTest(APITestCase):
    """
    댓글 읽어오기 테스트
    """
    @classmethod
    def setUpTestData(cls):
        cls.faker = Faker()
        cls.article_user = User.objects.create_user('test1','xptmxm123!')
        cls.article = Article.objects.create(category='일상', content='first content',user = cls.article_user)
        cls.comments = []
        mbti_list = ['ENFP', 'ENFJ', 'ENTP', 'ENTJ', 'ESFP', 'ESFJ', 'ESTP', 'ESTJ',
                        'INFP', 'INFJ', 'INTP', 'INTJ', 'ISFP', 'ISFJ', 'ISTP', 'ISTJ']
        for i in range(2,6):
            cls.comment_user = User.objects.create_user(cls.faker.name(), cls.faker.word())
            cls.comments.append(Comment.objects.create(
                content = cls.faker.sentence(),
                article_id = cls.article.id,
                user_id = cls.comment_user.id
                ))
            cls.user_chr = UserChr.objects.create(
                user_id = i,
                mbti = random.choice(mbti_list),
                gender = random.choice(['W','M']),
                age = random.randrange(10,80)
            )
            
    def test_get_comment(self):
        for comment in self.comments:
            url = reverse('comment_view', args=[self.article.id])
            response = self.client.get(url)
            serializer = CommentSerializer(comment).data
            print(serializer)
        # for key, value in serializer.items():
            # print(response.data['results'])
            # self.assertEqual(response.data['results'](key), value)
        
        self.assertEqual(response.status_code, 200)