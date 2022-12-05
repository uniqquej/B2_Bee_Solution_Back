from rest_framework import serializers
from article.models import Article,Comment,Solution
from article.models import Article, Solution, Rating

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('user','article','content')
        write_only_fields = ('content',)
        
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

        

