from rest_framework import serializers
from article.models import Article, Solution, Rating

class BeeSolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solution
        fields = ['wise','id'] # wise > solution_image로 변경할 것 
        read_only_fields=['id',] 
       
class WorrySerializer(serializers.ModelSerializer):
    solution=BeeSolutionSerializer(read_only = True)
    class Meta:
        model = Article
        fields=['category','content','mbti','solution']
         
class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields=['rating',]

        