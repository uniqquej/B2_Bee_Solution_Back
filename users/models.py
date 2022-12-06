from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

class UserManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError('Users must have an username')

        user = self.model(
            username = username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None):
        user = self.create_user(
            username=username,
            password=password,
            
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    username = models.CharField(max_length=50, blank=False, null=True, unique=True)
    profile_img = models.ImageField(default='profile_image/profile_default.jpg', upload_to='profile_image')

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username


    # custom 유저모델을 기본 유저모델로 사용하기 위한 필수코드
    def has_perm(self, perm, obj=None): # 권한이 있는지
        return True

    def has_module_perms(self, app_label):  # App의 모델에 접근가능 하도록 
        return True

    @property
    def is_staff(self): # 관리자 화면에 접근하도록
        return self.is_admin


class UserChr(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    mbti = models.CharField(max_length=4)
    age = models.IntegerField()
    gender = models.CharField(max_length=1)