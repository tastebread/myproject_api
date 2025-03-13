from django.urls import path
from .views import (
    PostListCreateView, PostDetailView,like_post,bookmark_post,
    liked_posts,bookmarked_posts,user_posts,comment_list_create,
    comment_delete
)

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
]