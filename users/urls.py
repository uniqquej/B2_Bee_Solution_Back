from django.urls import path
from users import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('signup/', views.UserCreateView.as_view(), name='user_create_view'),
    path('signin/', views.UserAuthView.as_view(), name='user_auth_view'),
    path('signout/', views.SignoutView.as_view(), name='user_signout_view'),
    # 토큰 발행
    path('api/token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('<int:user_id>/profile/', views.ProfileView.as_view(), name='profile_view'),
]