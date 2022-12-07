from rest_framework import serializers
from article.models import Article,Comment,Solution
from article.models import Article, Solution, Rating

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['user','article','content','id']
        read_only_fields=['id',]       
        
        
class BeeSolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solution
        fields = ['wise','id'] # wise > solution_image로 변경할 것 
        read_only_fields=['id',]
       
class WorrySerializer(serializers.ModelSerializer):
    solution=BeeSolutionSerializer(read_only = True)
    comment_set = CommentSerializer(many=True, read_only=True)
    class Meta:
        model = Article
        fields=['category','content','mbti','solution','id', 'comment_set']
        read_only_fields=['id',]
         
class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields=['rating',]

class MakeSolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solution
        fields = ['user','solution_image', 'wise', 'nickname']
        read_only_fields=['user',]