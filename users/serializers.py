from rest_framework import serializers
from users.models import User, UserChr
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from article.serializers import WorrySerializer, MakeSolutionSerializer
import re


class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = "__all__"

    def validate(self, data):
        is_password = re.compile(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@!%*#?&])[A-Za-z\d@!%*#?&]{8,}$')
         # 가입시 password 1 과 password2 가 일치하지 않을 때
        if data['password'] != data['password2']:
            raise serializers.ValidationError("password가 일치하지 않습니다.")
        
        elif not is_password.fullmatch(data['password']):
            raise serializers.ValidationError("비밀번호는 최소 8자리 이상의 숫자, 특수문자를 하나 이상 포함해야함")
        
        data.pop('password2') 
        return data
        
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


class ChangePasswordSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields=['password',]
        
    def validate(self, data):
        if 'password' in data:
            is_password = re.compile(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@!%*#?&])[A-Za-z\d@!%*#?&]{8,}$')
            if not is_password.fullmatch(data['password']):
                raise serializers.ValidationError("비밀번호는 최소 8자리 이상 숫자, 문자, 특수문자를 모두 포함해야함")
            return data
        
    def update(self, instance, validated_data):
        if "password" in validated_data:
            instance.set_password(validated_data.get('password', instance.password))
            instance.save()
        return instance