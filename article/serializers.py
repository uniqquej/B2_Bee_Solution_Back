from rest_framework import serializers
from article.models import Article,Comment,Solution
from article.models import Article, Solution, Rating
from users.models import User,UserChr

class commentUserchrSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserChr
        fields = ['user','mbti','age','gender']

class commentUserSerializer(serializers.ModelSerializer):
    userchr = commentUserchrSerializer(required=True)
    
    class Meta:
        model = User
        fields = ['userchr',]

class CommentSerializer(serializers.ModelSerializer):
    like_count = serializers.SerializerMethodField(read_only=True)
    
    def get_like_count(self, obj):
        return obj.likes.count()
    
    
    user = commentUserSerializer()
    class Meta:
        model = Comment
        fields = ['content','id','user','likes','like_count']
        read_only_fields=['id','user','likes',]       

class CommentcreateSerializer(serializers.ModelSerializer):
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
        fields = ['solution_image','id','user']
        read_only_fields=['id','user']
       
class WorrySerializer(serializers.ModelSerializer):
    comment_set = CommentSerializer(many=True, read_only=True)
    class Meta:
        model = Article
        fields=['category', 'content', 'mbti', 'id', 'comment_set', 'user', 'solution', 'new_comment']
        read_only_fields=['id', 'user', 'solution', 'new_comment']

class EditWorrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields=['category','content']
        
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


class MyRatingSolutionSerializer(serializers.ModelSerializer):
    solution = BeeSolutionSerializer(read_only = True)
    class Meta :
        model = Rating
        fields = ['rating', 'solution']