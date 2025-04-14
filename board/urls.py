from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import (
    PostListCreateView, PostDetailView,like_post,bookmark_post,
    liked_posts,bookmarked_posts,user_posts,comment_list_create,
    comment_delete,delete_multiple_post_images,my_posts,my_comments,my_liked_posts,my_liked_comments,
    my_bookmarked_posts,my_profile
)
#####
urlpatterns = [
    path('posts/', PostListCreateView.as_view(), name='post-list-create'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('posts/<int:post_id>/like/', like_post, name='post-like'),
    path('posts/<int:post_id>/bookmark/', bookmark_post, name='post-bookmark'),
    path('posts/liked/', liked_posts, name='liked-posts'),
    path('posts/bookmarked/', bookmarked_posts, name='bookmarked-posts'),
    path('users/<int:user_id>/posts/', user_posts, name='user-posts'),
    path('posts/<int:post_id>/comments/', comment_list_create, name='comment-list-create'),
    path('comments/<int:comment_id>/', comment_delete, name='comment-delete'),
    path('posts/<int:post_id>/delete-images/', delete_multiple_post_images, name='delete-multiple-images'),
    #마이페이지 관련 api
    path("mypage/posts/", my_posts, name="my_posts"),
    path("mypage/comments/", my_comments, name="my_comments"),
    path("mypage/liked-posts/", my_liked_posts, name="my_liked_posts"),
    path("mypage/liked-comments/", my_liked_comments, name="my_liked_comments"),
    path("mypage/bookmarked-posts/", my_bookmarked_posts, name="my_bookmarked_posts"),
    path("mypage/profile/", my_profile, name="my_profile"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)