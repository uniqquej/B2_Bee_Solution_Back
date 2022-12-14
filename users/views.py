from users.models import User
from users.serializers import UserSerializer, CustomTokenObtainPairSerializer, UserprofileSerializer, UserChrSerializer, UserChrCheckSerializer, ChangePasswordSerializer
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.generics import get_object_or_404
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from rest_framework.permissions import IsAuthenticated


class UserCreateView(APIView):
    def post(self, request): 
        serializer = UserSerializer(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"message":"가입완료!"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message":f"${serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)

class UserAuthView(APIView):
    def get(self, request):
        # token 있는데 signin.html 접속할 때
        try:
            access_token = request.headers['Authorization']
            if request.headers['Authorization'] is not None:
                token = request.headers['Authorization']
                refresh_token = str(token)
                access_token = str(token)
                
                if access_token:
                    return Response(
                        {
                            "refresh" : refresh_token,
                            "access": access_token
                        }, status=status.HTTP_200_OK)
            
        except:
            return Response({"message": "KEY_ERROR"}, status=400)
    
    def post(self, request):
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                user=User.objects.get(username=request.data['username'])
                password=request.data.get("password")
                # 존재하지 않는 유저일때
                if not user:
                    return Response({"message":f"존재하지 않는 유저입니다."}, status=status.HTTP_400_BAD_REQUEST)
        
                # 비밀번호가 틀렸을때
                if not check_password(password, user.password):
                    return Response({"message":f"잘못된 패스워드입니다."}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"message":f"잘못된 접근입니다."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            user = authenticate(username=request.data.get("username"), password=request.data.get("password"))
        
            if user.is_authenticated:
                token = CustomTokenObtainPairSerializer.get_token(user)
                refresh_token = str(token)
                access_token = str(token.access_token)
                return Response({"refresh" : refresh_token, "access": access_token}, status=status.HTTP_200_OK)
        
class SignoutView(APIView) :
    def post(self,request):
        response = Response()
        response.delete_cookie('jwt')
        return Response({"message": "로그아웃완료!"}, status=status.HTTP_204_NO_CONTENT)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer



class ProfileView(APIView):
    permissions_classes = [IsAuthenticated]
    
    def get(self, request, user_id):
        profile = get_object_or_404(User, id=user_id)
        serializer = UserprofileSerializer(profile)
        return Response(serializer.data)

    def put(self, request, user_id):
        profile = User.objects.get(id=user_id)
        update_serializer = UserprofileSerializer(profile, data=request.data)
        if update_serializer.is_valid():
            update_serializer.save()
            return Response(update_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"message":f"${update_serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user_id):
        profile_delete = User.objects.get(id=user_id)
        if request.user == profile_delete:
            request.user.delete()
            return Response({"message":"탈퇴완료!"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"message":"탈퇴실패!"}, status=status.HTTP_400_BAD_REQUEST)



class UserChrView(APIView):
    '''
    유저 캐릭터 생성
    '''
    # 유저 캐릭터 생성 체크
    def get(self, request, user_id):
        try:
            user = request.user
            if user.user_chr_check == False:
                return Response({"message":"유저캐릭터생성필요"}, status=status.HTTP_204_NO_CONTENT)
            return Response({"message":"유저 캐릭터 있음"}, status=status.HTTP_200_OK)
        except:
            return Response({"message":"잘못된 접근입니다"}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, user_id):
        user_chr_serializer = UserChrSerializer(data=request.data)
        if user_chr_serializer.is_valid():
            user_chr_serializer.save(user_id=user_id)
            print(user_chr_serializer)
            return Response({"message":"생성완료!"}, status=status.HTTP_200_OK)
        else:
            return Response({"message":f"${user_chr_serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        check_serializer = UserChrCheckSerializer(user, data=request.data)
        if check_serializer.is_valid():
            check_serializer.save()
            print(check_serializer)
            return Response({"message":"수정완료!"}, status=status.HTTP_200_OK)


class ChangePasswordView(APIView):
    permissions_classes = [IsAuthenticated]
     
    def put(self, request, user_id):
        user = User.objects.get(id = request.user.id)
        serializer = ChangePasswordSerializer(user, data = request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
