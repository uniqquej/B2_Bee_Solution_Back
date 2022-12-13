from rest_framework import serializers
from article.models import Article,Comment,Solution
from article.models import Article, Solution, Rating

class CommentSerializer(serializers.ModelSerializer):
    like_count = serializers.SerializerMethodField(read_only=True)
    
    def get_like_count(self, obj):
        return obj.likes.count()
    
    class Meta:
        model = Comment
        fields = ['content','id','user','likes','like_count']
        read_only_fields=['id','user','likes',]       
             
class BeeSolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solution
        fields = ['solution_image','id']
        read_only_fields=['id',]
       
class WorrySerializer(serializers.ModelSerializer):
    comment_set = CommentSerializer(many=True, read_only=True)
    class Meta:
        model = Article
        fields=['category','content','mbti','id', 'comment_set', 'user', 'solution']
        read_only_fields=['id','user', 'solution']
        
class SolutionDetailSerializer(serializers.ModelSerializer):
    solution = BeeSolutionSerializer(read_only = True, many=True)
    class Meta :
        model = Article
        fields = ['solution',]
                
class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields=['rating',]

class MakeSolutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solution
        fields = ['user','solution_image', 'wise', 'nickname']
        read_only_fields=['user',]