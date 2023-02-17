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
    
    
class CommentLikeTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.faker = Faker()
        cls.article_user = User.objects.create_user('test1','xptmxm123!')
        cls.current_user = User.objects.create_user('test2','xptmxm123!')
        cls.current_user_data = {"username":"test2", "password":"xptmxm123!"}
        cls.article = Article.objects.create(
            user_id = cls.article_user.pk,
            content = "article example",
            mbti = "ENFP",
            category = "일상"
        )
        
        for _ in range(3):
            Comment.objects.create(
                content = cls.faker.sentence(),
                article_id = cls.article.id,
                user_id = cls.current_user.id
                )
    
    def setUp(self):
        self.access_token = self.client.post(reverse('user_auth_view'), self.current_user_data).data['access']
    
    def test_like_comment(self):
        url = reverse('comment_like', kwargs={'article_id': 1, 'comment_id':1})
        response = self.client.post(
            path=url,
            HTTP_AUTHORIZATION = f'Bearer {self.access_token}'
        )
        
        self.assertEqual(response.data['message'],'좋아요')
        self.assertEqual(response.status_code,200)

class NewCommentAlarmTest(APITestCase):
    """
    게시글에 새로운 댓글 알림 기능 테스트
    """
    @classmethod
    def setUpTestData(cls):
        cls.faker = Faker()
        cls.user_data = {"username" :"article_user","password":"xptmxm123!"}
        cls.user = User.objects.create_user("article_user","xptmxm123!")
        cls.article = Article.objects.create(
            user_id = 1,
            content = cls.faker.sentence(),
            mbti = 'ENFP',
            category = '취업',
            new_comment = True
        )
        cls.comment = Comment.objects.create(
            article_id = 1,
            user_id = 1,
            content = cls.faker.sentence()
        )
    def setUp(self):
        self.access_token = self.client.post(reverse('user_auth_view'), self.user_data).data['access']
    
    def test_alarm_page(self):
        
        # 알람페이지에서 목록 확인
        url = reverse('alarm', args=[0])
        response = self.client.get(
            path = url,
            HTTP_AUTHORIZATION = f'Bearer {self.access_token}'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['content'],Article.objects.get(id=1).content)
    
    def test_comment_alarm(self):
        
        # 다른 페이지에서 알림 이미지 상태
        url = reverse('alarm', args=[1])
        response = self.client.get(
            path = url,
            HTTP_AUTHORIZATION = f'Bearer {self.access_token}'
        )

        self.assertEqual(response.status_code, 200)
        
        
        