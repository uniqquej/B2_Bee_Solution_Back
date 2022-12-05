from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from similarity import make_solution
from makesolution import make_wise_image
from article.models import Solution
from article.serializers import WorrySerializer, BeeSolutionSerializer, RatingSerializer, MakeSolutionSerializer


class MakeWorryView(APIView):
    def post(self, request):
        
        my_id = request.user.id
        result = make_solution(my_id)
        print(result)
        
        worry_serializer = WorrySerializer(data = request.data)
        if worry_serializer.is_valid():
            worry_serializer.save(user=request.user, solution_id= result)
            return Response(worry_serializer.errors)
        
        return Response({"message":"성공", "solution_id":result})
    
   
class BeeSolutionView(APIView):  
    def get(self,request, solution_id):
        bee_solution = Solution.objects.get(id = solution_id)
        bee_solution_serializer = BeeSolutionSerializer(bee_solution)
        return Response(bee_solution_serializer.data, status=status.HTTP_200_OK)
    
    def post(self,request,solution_id):
        rating_serializer = RatingSerializer(data = request.data)
        if rating_serializer.is_valid():
            rating_serializer.save(user = request.user, solution_id = solution_id)
            return Response({"message":"성공"}, status=status.HTTP_200_OK)
        return Response(rating_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MakeSolutionView(APIView):
    def get(self, request, article_id):
        pass
    
    def post(self, request, article_id):
        make_solution_serializer = MakeSolutionSerializer(data=request.data)
        if make_solution_serializer.is_valid():
            make_solution_serializer.save(user=request.user)
            
            latest_idx = Solution.objects.order_by('-pk')[0].pk
            makewisepicture(latest_idx)
            
            return Response("저장 완료", status=status.HTTP_200_OK)
        else:
            return Response("실패", status=status.HTTP_400_BAD_REQUEST)