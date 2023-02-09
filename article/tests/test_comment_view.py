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
        cls.article = Article.objects.create(category='일상', content='first content', user = cls.user)
    
    def setUp(self): # 매 테스트마다 실행
       self.access_token = self.client.post(reverse('user_auth_view'), self.user_data).data['access']
    
    def test_create_comment(self):
        url = reverse('comment_view', args=[self.article.id])
        response = self.client.post(
            path = url, 
            data = {'content':"1등이야"},
            HTTP_AUTHORIZATION = f"Bearer {self.access_token}")
        # print(response.data)
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
        for idx,comment in enumerate(reversed(self.comments)):
            url = reverse('comment_view', args=[self.article.id])
            response = self.client.get(url)
            serializer = CommentSerializer(comment).data
        
            for key, value in serializer.items():
                self.assertEqual(response.data['results'][idx][key], value)
        
        self.assertEqual(response.status_code, 200)

class CommentDetailTest(APITestCase):
    '''
    댓글 수정, 삭제 테스트
    '''
    @classmethod
    def setUpTestData(cls):
        cls.faker = Faker()
        cls.article_user = User.objects.create_user('test1','xptmxm123!')
        cls.article = Article.objects.create(category='일상', content='first content',user = cls.article_user)
        cls.comments = []
        mbti_list = ['ENFP', 'ENFJ', 'ENTP', 'ENTJ', 'ESFP', 'ESFJ', 'ESTP', 'ESTJ',
                        'INFP', 'INFJ', 'INTP', 'INTJ', 'ISFP', 'ISFJ', 'ISTP', 'ISTJ']
        for i in range(2,6):
            cls.comment_user = User.objects.create_user(cls.faker.name(), 'xptmxm123!')
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
    
    def test_edit_comment(self):
        '''
        댓글 유저와 현재 유저가 일치할 경우
        '''
        self.current_user = User.objects.get(id = 2)
        self.access_token = self.client.post(reverse('user_auth_view'),{'username':self.current_user, 'password':'xptmxm123!'}).data['access']
        
        url = reverse('comment_detail', kwargs={'article_id': 1, 'comment_id':1})
        response = self.client.put(
            path = url, 
            data = {'content':'edit comment!!'},
            HTTP_AUTHORIZATION = f'Bearer {self.access_token}'
            )
        # print(self.current_user)
        # print(Comment.objects.get(id = 1).user)
        self.assertEqual(response.status_code, 200)
    
    def test_edit_comment_case2(self):
        '''
        댓글 유저와 현재 유저가 일치하지 않는 경우
        '''
        self.current_user = User.objects.get(id = 2)
        self.access_token = self.client.post(reverse('user_auth_view'),{'username':self.current_user, 'password':'xptmxm123!'}).data['access']
        
        url = reverse('comment_detail', kwargs={'article_id': 1, 'comment_id':2})
        response = self.client.put(
            path = url, 
            data = {'content':'edit comment!!'},
            HTTP_AUTHORIZATION = f'Bearer {self.access_token}'
            )

        self.assertEqual(response.status_code, 403)
    
    def test_delet_comment(self):
        '''
        댓글 유저와 현재 유저가 일치할 경우
        '''
        self.current_user = User.objects.get(id = 2)
        self.access_token = self.client.post(reverse('user_auth_view'),{'username':self.current_user, 'password':'xptmxm123!'}).data['access']
        
        url = reverse('comment_detail', kwargs={'article_id': 1, 'comment_id':1})
        response = self.client.delete(
            path = url, 
            HTTP_AUTHORIZATION = f'Bearer {self.access_token}'
            )
        # print(self.current_user)
        # print(Comment.objects.get(id = 1).user)
        self.assertEqual(response.status_code, 200)
    
    def test_edit_delete_case2(self):
        '''
        댓글 유저와 현재 유저가 일치하지 않는 경우
        '''
        self.current_user = User.objects.get(id = 2)
        self.access_token = self.client.post(reverse('user_auth_view'),{'username':self.current_user, 'password':'xptmxm123!'}).data['access']
        
        url = reverse('comment_detail', kwargs={'article_id': 1, 'comment_id':2})
        response = self.client.delete(
            path = url, 
            HTTP_AUTHORIZATION = f'Bearer {self.access_token}'
            )

        self.assertEqual(response.status_code, 403)
    