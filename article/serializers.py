from rest_framework import serializers
from article.models import Article,Comment,Solution

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('user','article','content')
        write_only_fields = ('content',)
        

