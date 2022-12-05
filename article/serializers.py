from rest_framework import serializers
from article.models import Article, Solution, Rating

class WorrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields=['category','content','mbti']

class BeeSolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solution
        fields = ['wise',]
        
class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields=['rating',]

class MakeSolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solution
        fields = ['solution_image',]