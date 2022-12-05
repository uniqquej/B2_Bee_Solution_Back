from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from similarity import make_solution
from article.models import Solution,  Article
from article.serializers import WorrySerializer,BeeSolutionSerializer, RatingSerializer

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


        