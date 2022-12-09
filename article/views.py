from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from similarity import make_solution
from makesolution import make_wise_image
from article.models import Solution, Article, Rating, Comment
from article.serializers import WorrySerializer,BeeSolutionSerializer, RatingSerializer, CommentSerializer, MakeSolutionSerializer
from rest_framework.pagination import PageNumberPagination 
from article.pagination import PaginationHandlerMixin

class ArticlePagination(PageNumberPagination): # 한 페이지에 게시물 3개
    page_size = 3
    
class MakeWorryView(APIView):
    def post(self, request):
        my_id = request.user.id
        result = make_solution(my_id)
        worry_serializer = WorrySerializer(data=request.data)
        if worry_serializer.is_valid():
            thisarticle = worry_serializer.save(user=request.user)
            thisarticle.solution.add(result)
            return Response(worry_serializer.data, status=status.HTTP_200_OK)
        return Response(worry_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        solution = Article.objects.filter(user_id = request.user.id).last()
        solution_serializer = WorrySerializer(solution)
        return Response(solution_serializer.data, status=status.HTTP_200_OK)
      
class BeeSolutionView(APIView):  
    def get(self,request, solution_id):
        bee_solution = Solution.objects.get(id = solution_id)
        bee_solution_serializer = BeeSolutionSerializer(bee_solution)
        return Response(bee_solution_serializer.data, status=status.HTTP_200_OK)
    
    def post(self,request,solution_id):
        rating_serializer = RatingSerializer(data = request.data)
        if rating_serializer.is_valid():
            #같은 유저가 같은 솔루션을 평가했는지 체크
            if Rating.objects.filter(user_id = request.user.id, solution_id = solution_id).exists():
                Rating.objects.filter(user_id = request.user.id, solution_id = solution_id).delete()
                rating_serializer.save(user = request.user, solution_id = solution_id)
                return Response({"message":"평가 완료"}, status=status.HTTP_200_OK)
            else:
                rating_serializer.save(user = request.user, solution_id = solution_id)
                return Response({"message":"평가 완료"}, status=status.HTTP_200_OK)
        return Response(rating_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentView(APIView):
    def get(self,request,article_id):
        article=  Article.objects.get(id=article_id)
        comments = article.comment_set.all()
        comment_serializer = CommentSerializer(comments,many=True)
        return Response(comment_serializer.data,status=status.HTTP_200_OK)
    
    def post(self,request,article_id):
        comment_serializer = CommentSerializer(data=request.data)
        if comment_serializer.is_valid():
            comment_serializer.save(user = request.user, article_id = article_id)
            return Response(comment_serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(comment_serializer.errors,status=status.HTTP_400_BAD_REQUEST)    

class CommentDetailView(APIView):
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
    def post(self, request, article_id):
        make_solution_serializer = MakeSolutionSerializer(data=request.data)
        if make_solution_serializer.is_valid():
            thissolution = make_solution_serializer.save(user=request.user)
            make_wise_image(thissolution.pk)
            start_rating = Rating(user_id=request.user.id, solution_id =thissolution.pk, rating=4)
            start_rating.save()
            return Response("저장 완료", status=status.HTTP_200_OK)
        else:
            return Response("실패", status=status.HTTP_400_BAD_REQUEST)

class ArticleDetailView(APIView):
    def get(self,request,article_id):
        article_detail = Article.objects.get(id=article_id)
        article_detail_serializer = WorrySerializer(article_detail)
        return Response(article_detail_serializer.data,status=status.HTTP_200_OK)
    
    def put(self,request,article_id):
        aritcle = Article.objects.get(id= article_id)
        article_serializer = WorrySerializer(aritcle,data=request.data)
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
    pagination_class = ArticlePagination
    serializer_class = WorrySerializer
    
    def get(self, request, category_id):
        if 0 < category_id < 9 :
            category_list = ['음식','취미','취업','일상','투자','연애','스포츠','연예']
            category = category_list[category_id - 1]
        elif category_id >= 9:
            mbti_list = ['ENFP','ENFJ','ENTP','ENTJ','ESFP','ESFJ','ESTP','ESTJ',
                        'INFP','INFJ','INTP','INTJ','ISFP','ISFJ','ISTP','ISTJ']
            mbti = mbti_list[category_id - 9]
        
        if category_id == 0:
            articles = Article.objects.all()
            
        elif category_id < 9:
            articles = Article.objects.filter(category = category)
        else:
            articles = Article.objects.filter(mbti=mbti)
        
        page = self.paginate_queryset(articles)

        if page is not None:
            serializer = self.get_paginated_response(self.serializer_class(page, many=True).data)
        else:
            serializer = self.serializer_class(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)