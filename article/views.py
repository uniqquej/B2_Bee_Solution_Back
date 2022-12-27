from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from similarity import make_solution
from makesolution import make_wise_image
from article.models import Solution, Article, Rating, Comment
from article.serializers import EditWorrySerializer,WorrySerializer,BeeSolutionSerializer, RatingSerializer, CommentSerializer, MakeSolutionSerializer, SolutionDetailSerializer, MyRatingSolutionSerializer
from rest_framework.pagination import PageNumberPagination 
from article.pagination import PaginationHandlerMixin
from users.models import User, UserChr

class ArticlePagination(PageNumberPagination):
    page_size = 3
    
class CommentPagination(PageNumberPagination): 
    page_size = 5
    
class MakeWorryView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        my_id = request.user.id
        category_list = ['일상','취미','취업','음식']
        category = category_list.index(request.data['category'])+1
        
        worry_serializer = WorrySerializer(data=request.data)
        if worry_serializer.is_valid():
            result = make_solution(my_id, category)
            thisarticle = worry_serializer.save(user=request.user, new_comment=0)
            thisarticle.solution.add(result)
            return Response(worry_serializer.data, status=status.HTTP_200_OK)
        return Response(worry_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        solution = Article.objects.filter(user_id=request.user.id).first()
        solution_serializer = WorrySerializer(solution)
        return Response(solution_serializer.data, status=status.HTTP_200_OK)
      
class BeeSolutionView(APIView):  
    permission_classes = [IsAuthenticated]
    
    def get(self,request, solution_id):
        bee_solution = Solution.objects.get(id = solution_id)
        bee_solution_serializer = BeeSolutionSerializer(bee_solution)
        return Response(bee_solution_serializer.data, status=status.HTTP_200_OK)

class CommentView(APIView,PaginationHandlerMixin):
    # permission_classes = [IsAuthenticated]
    
    pagination_class = CommentPagination
    serializer_class = CommentSerializer 
    def get(self,request,article_id):
        article=  Article.objects.get(id=article_id)        
        comments = article.comment_set.all()
        page = self.paginate_queryset(comments)
        if page is not None:
            serializer = self.get_paginated_response(self.serializer_class(page,many=True).data)
        else:
            serializer = self.get_paginated_response(comments,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def post(self,request,article_id):
        comment_serializer = CommentSerializer(data=request.data)
        if comment_serializer.is_valid():
            this_comment = comment_serializer.save(user=request.user, article_id=article_id)
            this_article = Article.objects.get(id=this_comment.article_id)
            this_article.new_comment = 1
            this_article.save()
            return Response(comment_serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(comment_serializer.errors,status=status.HTTP_400_BAD_REQUEST)    

class CommentDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    def put(self,request,article_id,comment_id):
        comment = Comment.objects.get(id=comment_id)
        if request.user == comment.user:
            comment_serializer = CommentSerializer(comment,data=request.data)
            if comment_serializer.is_valid():
                comment_serializer.save()
                return Response(comment_serializer.data,status=status.HTTP_200_OK)
            else:
                return Response({"message":"권한이 없습니다."},status=status.HTTP_403_FORBIDDEN)
    
    def delete(self,request,article_id,comment_id):
        comment = Comment.objects.get(id=comment_id)
        if request.user == comment.user:
            comment.delete()
            return Response({"message":"삭제 되었습니다."},status=status.HTTP_200_OK)
        else:
            return Response({"message":"권한이 없습니다."},status=status.HTTP_403_FORBIDDEN)

class MakeSolutionView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, article_id):
        article=  Article.objects.get(id=article_id)
        solution_serializer = SolutionDetailSerializer(article)
        return Response(solution_serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, article_id):
        make_solution_serializer = MakeSolutionSerializer(data=request.data)
        if make_solution_serializer.is_valid():
            thissolution = make_solution_serializer.save(user=request.user)
            make_wise_image(thissolution.pk)
            start_rating = Rating(user_id=request.user.id, solution_id =thissolution.pk, rating=4)
            start_rating.save()

            request_category = request.data['category']
            for i in request_category:
                thissolution.category.add(i)
            
            if article_id:
                article = Article.objects.get(id=article_id)
                article.solution.add(thissolution.pk)
            
            return Response("저장 완료", status=status.HTTP_200_OK)
        else:
            return Response("실패", status=status.HTTP_400_BAD_REQUEST)
        
class SolutionDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, solution_id):
        solution_detail_serializer = RatingSerializer(data = request.data)
        if solution_detail_serializer.is_valid():
            #같은 유저가 같은 솔루션을 평가했는지 체크
            if Rating.objects.filter(user_id = request.user.id, solution_id = solution_id).exists():
                Rating.objects.filter(user_id = request.user.id, solution_id = solution_id).delete()
                solution_detail_serializer.save(user = request.user, solution_id = solution_id)
                return Response({"message":"평가 완료"}, status=status.HTTP_200_OK)
            else:
                solution_detail_serializer.save(user = request.user, solution_id = solution_id)
                return Response({"message":"평가 완료"}, status=status.HTTP_200_OK)
        return Response(solution_detail_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, solution_id):
        solution = Solution.objects.get(id=solution_id)
        if request.user == solution.user:
            solution.delete()
            return Response({"message":"삭제 되었습니다."},status=status.HTTP_200_OK)
        else:
            return Response({"message":"권한이 없습니다."},status=status.HTTP_403_FORBIDDEN)
    
    

class ArticleDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self,request,article_id):
        article_detail = Article.objects.get(id=article_id)
        article_detail_serializer = WorrySerializer(article_detail)
        if request.user == article_detail.user:
            article_detail.new_comment = 0
            article_detail.save()
        return Response(article_detail_serializer.data,status=status.HTTP_200_OK)
    
    def put(self,request,article_id):
        aritcle = Article.objects.get(id= article_id)
        article_serializer = EditWorrySerializer(aritcle,data=request.data)
        if request.user == aritcle.user:
            if article_serializer.is_valid():
                article_serializer.save()
                return Response(article_serializer.data,status=status.HTTP_200_OK)
            else:
                return Response(article_serializer.errors,status=status.__name__)
        else:
            return Response({"message":"권한이 없습니다."},status=status.HTTP_403_FORBIDDEN)
    
    def delete(self,request,article_id):
        article_delete = Article.objects.get(id=article_id)
        if request.user == article_delete.user:
            article_delete.delete()
            return Response({"message":"삭제 완료"},status=status.HTTP_200_OK)
        else:
            return Response({"message":"권한이 없습니다."},status=status.HTTP_403_FORBIDDEN)
        
class MainView(APIView, PaginationHandlerMixin):
    permission_classes = [IsAuthenticated]
    
    pagination_class = ArticlePagination
    serializer_class = WorrySerializer
    
    def get(self, request, category_id):
        if 0 < category_id < 5 :
            category_list = ['일상','취미','취업','음식']
            category = category_list[category_id - 1]
        elif category_id >= 9:
            mbti_list = ['ENFP','ENFJ','ENTP','ENTJ','ESFP','ESFJ','ESTP','ESTJ',
                        'INFP','INFJ','INTP','INTJ','ISFP','ISFJ','ISTP','ISTJ']
            mbti = mbti_list[category_id - 9]
        
        if category_id == 0:
            articles = Article.objects.all()
            
        elif category_id < 5:
            articles = Article.objects.filter(category = category)
        else:
            articles = Article.objects.filter(mbti=mbti)
        
        page = self.paginate_queryset(articles)

        if page is not None:
            serializer = self.get_paginated_response(self.serializer_class(page, many=True).data)
        else:
            serializer = self.serializer_class(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class AllBeeSolutionView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        bee_solution = Solution.objects.all().order_by('-pk')
        bee_solution_serializer = BeeSolutionSerializer(bee_solution, many = True)
        return Response(bee_solution_serializer.data, status=status.HTTP_200_OK)


class MyBeeSolutionView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        bee_solution = Rating.objects.filter(user_id = request.user).order_by('-pk')
        bee_solution_serializer = MyRatingSolutionSerializer(bee_solution, many = True)
        return Response(bee_solution_serializer.data, status=status.HTTP_200_OK)


class CommentLikeView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request,article_id,comment_id):
        me = request.user
        comment = Comment.objects.get(id = comment_id)
        if me in comment.likes.all():
            comment.likes.remove(me)
            return Response({"message":"좋아요취소"}, status=status.HTTP_200_OK)
        else:
            comment.likes.add(me)
            return Response({"message":"좋아요"}, status=status.HTTP_200_OK)


class ProfileArticleView(APIView, PaginationHandlerMixin):
    permission_classes = [IsAuthenticated]
    
    pagination_class = ArticlePagination
    serializer_class = WorrySerializer
    
    def get(self, request, category_id):
        
        if 0 < category_id < 5 :
            category_list = ['일상','취미','취업','음식']
            category = category_list[category_id - 1]
        elif category_id >= 9:
            mbti_list = ['ENFP','ENFJ','ENTP','ENTJ','ESFP','ESFJ','ESTP','ESTJ',
                        'INFP','INFJ','INTP','INTJ','ISFP','ISFJ','ISTP','ISTJ']
            mbti = mbti_list[category_id - 9]
        
        if category_id == 0:
            articles = Article.objects.filter(user = request.user)
            
        elif category_id < 5:
            articles = Article.objects.filter(category = category, user = request.user)
        else:
            articles = Article.objects.filter(mbti=mbti, user = request.user)
        
        page = self.paginate_queryset(articles)

        if page is not None:
            serializer = self.get_paginated_response(self.serializer_class(page, many=True).data)
        else:
            serializer = self.serializer_class(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
class AlarmView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        new_comment_article = Article.objects.filter(user=request.user, new_comment=True)
        new_comment_article_serializer = WorrySerializer(new_comment_article, many=True)
        return Response(new_comment_article_serializer.data, status=status.HTTP_200_OK)

class MakeWorryPromotionView(APIView):
    def post(self, request):
        # 내가 선택한 MBTI 와 같은 MBTI 를 지니고 있는 유저 중 첫번째 유저 선택
        promotion_mbti = request.data['mbti']
        my_id = UserChr.objects.filter(mbti=promotion_mbti).first().user_id
        if my_id is None:
            my_id = 115
        category_list = ['일상','취미','취업','음식']
        category = category_list.index(request.data['category'])+1
        result = make_solution(my_id, category)
        data = Solution.objects.filter(id = result).values()
        
        return Response({'data': data}, status=status.HTTP_200_OK)