from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from similarity import make_solution
from makesolution import make_wise_image
from article.models import Solution, Comment, Article
from article.serializers import WorrySerializer,BeeSolutionSerializer, RatingSerializer, CommentSerializer, MakeSolutionSerializer


class MakeWorryView(APIView):
    def post(self, request):
        
        my_id = request.user.id
        result = make_solution(my_id)

        worry_serializer = WorrySerializer(data = request.data)
        if worry_serializer.is_valid():
            worry_serializer.save(user=request.user, solution_id= result)
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
            comment_serializer.save(comment_user = request.user, article_id = article_id)
            return Response(comment_serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(comment_serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class MakeSolutionView(APIView):
    def get(self, request, article_id):
        pass
    
    def post(self, request, article_id):
        make_solution_serializer = MakeSolutionSerializer(data=request.data)
        if make_solution_serializer.is_valid():
            make_solution_serializer.save(user=request.user)
            
            latest_idx = Solution.objects.order_by('-pk')[0].pk
            make_wise_image(latest_idx)
            
            return Response("저장 완료", status=status.HTTP_200_OK)
        else:
            return Response("실패", status=status.HTTP_400_BAD_REQUEST)

class MainView(APIView):
    def get(self,request):
        main_articles = Article.objects.all()
        main_serializer = WorrySerializer(main_articles,many=True)
        return Response(main_serializer.data,status=status.HTTP_200_OK)

