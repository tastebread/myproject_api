from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import send_mail
from django.conf import settings

from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Profile,Follow


#API에서 데이터를 JSON으로 변환하는 역할
User = get_user_model()

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('bio', 'profile_image', 'created_at')

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ('id', 'email', 'username','profile')
    
    def update(self, instance, validated_data):
        """사용자 및 프로필 정보를 업데이트하는 메서드"""
        profile_data = validated_data.pop('profile', None)  # 프로필 데이터 분리
        instance.username = validated_data.get('username', instance.username)
        instance.save()

        if profile_data:
            profile = instance.profile
            profile.bio = profile_data.get('bio', profile.bio)
            profile.profile_image = profile_data.get('profile_image', profile.profile_image)
            profile.save()

        return instance

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password']
        )
        Profile.objects.create(user=user) #회원가입시 프로필 자동생성
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = User.objects.filter(email=data['email']).first()
        if user and user.check_password(data['password']):
            refresh = RefreshToken.for_user(user)
            return {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
            }
        raise serializers.ValidationError("Invalid credentials")

#비밀번호 변경
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password1 = serializers.CharField(write_only=True)
    new_password2 = serializers.CharField(write_only=True)

    def validate(self, data):
        user = self.context['request'].user

        # 현재 비밀번호가 올바른지 확인
        if not user.check_password(data['old_password']):
            raise serializers.ValidationError({"old_password": "현재 비밀번호가 올바르지 않습니다."})

        # 새로운 비밀번호 확인
        if data['new_password1'] != data['new_password2']:
            raise serializers.ValidationError({"new_password2": "새로운 비밀번호가 일치하지 않습니다."})

        return data

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password1'])  # 비밀번호 변경
        user.save()
        return user


#비밀번호 재설정 (이메일 전송)
class ResetPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, data):
        email = data['email']
        user = User.objects.filter(email=email).first()
        if not user:
            raise serializers.ValidationError({"email": "이 이메일을 사용하는 계정이 없습니다."})

        # 토큰 생성
        uidb64 = urlsafe_base64_encode(str(user.pk).encode('utf-8'))
        token = PasswordResetTokenGenerator().make_token(user)

        # 비밀번호 재설정 URL 생성 (프론트엔드 URL로 연결 가능)
        reset_url = f"{settings.FRONTEND_URL}/reset-password/{uidb64}/{token}/"

        # 이메일 전송
        send_mail(
            "비밀번호 재설정 요청",
            f"안녕하세요! 비밀번호 재설정을 위해 아래 링크를 클릭하세요:\n{reset_url}",
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )

        return data

#비밀번호 재 설정
class SetNewPasswordSerializer(serializers.Serializer):
    uidb64 = serializers.CharField()
    token = serializers.CharField()
    new_password1 = serializers.CharField(write_only=True)
    new_password2 = serializers.CharField(write_only=True)

    def validate(self, data):
        try:
            uid = force_str(urlsafe_base64_decode(data['uidb64']))
            user = User.objects.get(pk=uid)

            if not PasswordResetTokenGenerator().check_token(user, data['token']):
                raise serializers.ValidationError({"token": "토큰이 유효하지 않거나 만료되었습니다."})

            if data['new_password1'] != data['new_password2']:
                raise serializers.ValidationError({"new_password2": "새로운 비밀번호가 일치하지 않습니다."})

            user.set_password(data['new_password1'])
            user.save()

        except (DjangoUnicodeDecodeError, User.DoesNotExist):
            raise serializers.ValidationError({"error": "잘못된 요청입니다."})

        return data

#이미지

class ProfileSerializer(serializers.ModelSerializer):
    profile_image = serializers.ImageField(required=False)  # 이미지 필드 추가

    class Meta:
        model = Profile
        fields = ('bio', 'profile_image', 'created_at')

class ProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('profile_image',)

#유저검색
class UserSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'profile')  # 프로필 정보 포함

#팔로우

class FollowSerializer(serializers.ModelSerializer):
    follower = serializers.ReadOnlyField(source="follower.username")  # 현재 로그인한 사용자
    following = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field="username"
    )

    class Meta:
        model = Follow
        fields = ('follower', 'following', 'created_at')