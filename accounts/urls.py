from django.urls import path
from .views import RegisterView, LoginView,ProfileView,ChangePasswordView
from .views import ResetPasswordRequestView, SetNewPasswordView,ProfileImageUploadView
from .views import UserSearchView,FollowView,UnfollowView,FollowingListView,FollowersListView,LogoutView
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'), #회원가입
    path('login/', LoginView.as_view(), name='login'), # 로그인
    path('profile/', ProfileView.as_view(), name='profile'),  # 프로필 조회 & 수정
    path('change-password/', ChangePasswordView.as_view(), name='change-password'), #비밀번호변경
    path('reset-password/', ResetPasswordRequestView.as_view(), name='reset-password-request'),#이메일
    path('reset-password/confirm/', SetNewPasswordView.as_view(), name='set-new-password'),#재설정
    path('profile/upload-image/', ProfileImageUploadView.as_view(), name='profile-image-upload'), #프로필이미지
    path('search/', UserSearchView.as_view(), name='user-search'),
    path('follow/', FollowView.as_view(), name='follow'),
    path('unfollow/', UnfollowView.as_view(), name='unfollow'),
    path('following/', FollowingListView.as_view(), name='following-list'),
    path('followers/', FollowersListView.as_view(), name='followers-list'),
    path('logout/', LogoutView.as_view(), name='logout'),
]