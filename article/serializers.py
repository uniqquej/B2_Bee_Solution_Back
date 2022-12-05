from rest_framework import serializers
from article.models import Article

class ArticleSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_article_user(self, obj):
        return obj.user.username

    class Meta:
        model = Article
        fields = ("user", "category", "solution", "content", "mbti")
        
