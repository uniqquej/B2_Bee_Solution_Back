from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from similarity import make_solution

class SolutionView(APIView):
    def get(self, request):

        my_id = request.user.id
        result = make_solution(my_id)
        print(result)
        
        return Response({"message":"성공", "solution_id":result})