from rest_framework import serializers
from users.models import User
from article.views import ArticleSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('followings',)

    def create(self, validated_data):   
        user = super().create(validated_data)
        password = user.password
        user.set_password(password)
        user.save()
        return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username

        return token



class UserprofileSerializer(serializers.ModelSerializer):
    article_set = ArticleSerializer(many=True)

    class Meta:
        model = User
        fields = ("username", 'profile_img', 'article_set')