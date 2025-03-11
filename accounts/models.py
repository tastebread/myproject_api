from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    
    USERNAME_FIELD = 'email'  # 기본 로그인 필드를 이메일로 변경 (수정될수 있음
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

#프로필 모델
class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)  # 자기소개
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)  # 가입 날짜

    def __str__(self):
        return f"{self.user.username}'s Profile"

#팔로우 관계 (친구추가)
class Follow(models.Model):
    follower = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="following")
    following = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="followers")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')  # 중복 팔로우 방지

    def __str__(self):
        return f"{self.follower.username} → {self.following.username}"