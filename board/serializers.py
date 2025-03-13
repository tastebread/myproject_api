from rest_framework import serializers
from .models import Post, Like,Bookmark,Comment

#댓글
class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.username", read_only=True)  # 작성자 이름 추가

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'author_name', 'content', 'created_at']
        read_only_fields = ['id', 'author', 'created_at']

#직렬화
class PostSerializer(serializers.ModelSerializer):
    
    likes_count = serializers.IntegerField(source='liked_by.count', read_only=True)  # 좋아요 개수 추가
    bookmarks_count = serializers.IntegerField(source='bookmarked_by.count', read_only=True) # 북마크 갯수 추가
    comments = CommentSerializer(many=True, read_only=True) # 댓글 ㅗ함

    class Meta:
        model = Post
        fields = ['id', 'author', 'title', 'content','tags', 'created_at', 'updated_at']
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'post', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']

class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = ['id', 'user', 'post', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']
