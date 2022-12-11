from rest_framework import serializers
from users.models import User, UserChr
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from article.serializers import WorrySerializer, MakeSolutionSerializer
import django.contrib.auth.password_validation as validate_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


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
    article_set = WorrySerializer(read_only = True, many=True)
    solution_set = MakeSolutionSerializer(read_only = True, many=True)

    class Meta:
        model = User
        fields = ["username", 'profile_img', 'article_set', 'solution_set']
        
        
class UserChrSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserChr
        fields = ["mbti", "age", "gender"]
        read_only_fields = ['user',]
        
class UserChrCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('user_chr_check',)


# username 변경
class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', )

    def validate_username(self, value):
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(username=value).exists():
            raise serializers.ValidationError({"username": "This username is already in use."})
        return value

    def put(self, instance, validated_data):
        user = self.context['request'].user

        if user.pk != instance.pk:
            raise serializers.ValidationError({"authorize": "You dont have permission for this user."})

        instance.username = validated_data['username']
        instance.save()
        return instance