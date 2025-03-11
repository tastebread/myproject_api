from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import generics,status,filters
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenRefreshView
from django.contrib.auth import get_user_model
from .models import Profile,Follow
from .serializers import RegisterSerializer, LoginSerializer,UserSerializer,ChangePasswordSerializer
from .serializers import ResetPasswordRequestSerializer, SetNewPasswordSerializer,ProfileImageSerializer
from .serializers import UserSearchSerializer,FollowSerializer

User = get_user_model()

#사용자 회원가입
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

#사용자 로그인
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)

#프로필
class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

#비밀번호 변경 
class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]  # 로그인된 사용자만 가능

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "비밀번호가 성공적으로 변경되었습니다."}, status=status.HTTP_200_OK)

#비밀번호 재설정 (이메일)
class ResetPasswordRequestView(generics.GenericAPIView):
    serializer_class = ResetPasswordRequestSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"message": "비밀번호 재설정 이메일이 전송되었습니다."}, status=status.HTTP_200_OK)

#비밀번호 재설정
class SetNewPasswordView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"message": "비밀번호가 성공적으로 변경되었습니다."}, status=status.HTTP_200_OK)
    
#프로필 이미지

class ProfileImageUploadView(generics.UpdateAPIView):
    serializer_class = ProfileImageSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)  # 파일 업로드를 처리

    def get_object(self):
        return self.request.user.profile  # 현재 로그인한 사용자의 프로필 반환

#유저검색
class UserSearchView(generics.ListAPIView):
    serializer_class = UserSearchSerializer
    permission_classes = [IsAuthenticated]  # 로그인된 사용자만 검색 가능
    queryset = User.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'email']  # 필드기준으로 검색 가능

#유저 팔로우
class FollowView(generics.CreateAPIView):
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        following = get_object_or_404(User, username=request.data.get('following'))
        
        if Follow.objects.filter(follower=request.user, following=following).exists():
            return Response({"error": "이미 팔로우하고 있습니다."}, status=status.HTTP_400_BAD_REQUEST)

        Follow.objects.create(follower=request.user, following=following)
        return Response({"message": f"{following.username}님을 팔로우했습니다."}, status=status.HTTP_201_CREATED)

#유저 언팔로우
class UnfollowView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        following = get_object_or_404(User, username=request.data.get('following'))
        follow = Follow.objects.filter(follower=request.user, following=following).first()

        if not follow:
            return Response({"error": "팔로우하지 않은 사용자입니다."}, status=status.HTTP_400_BAD_REQUEST)

        follow.delete()
        return Response({"message": f"{following.username}님을 언팔로우했습니다."}, status=status.HTTP_200_OK)

#내가팔로우하는 유저 리스트
class FollowingListView(generics.ListAPIView):
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Follow.objects.filter(follower=self.request.user)

#나를 팔로우하는 유저 리스트
class FollowersListView(generics.ListAPIView):
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Follow.objects.filter(following=self.request.user)

#로그아웃 뷰
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()  # Refresh 토큰을 블랙리스트에 추가
            return Response({"message": "로그아웃되었습니다."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": "잘못된 토큰입니다."}, status=status.HTTP_400_BAD_REQUEST)