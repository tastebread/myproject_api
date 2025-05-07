from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import MultiPartParser, FormParser,JSONParser
from .models import Post,Like,Bookmark,PostImage,Comment
from .serializers import PostSerializer,LikeSerializer,BookmarkSerializer,CommentSerializer,PostSerializer, PostImageSerializer
from django.core.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model

User = get_user_model()

#목록 조회 ,게시글 작성
class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]
    parser_classes = [JSONParser, MultiPartParser, FormParser]
    filter_backends = [DjangoFilterBackend]
    search_fields = ['title', 'content'] #검색 가능 필드
    ordering_fields = ['created_at'] #정렬 가능 필드

    def get_queryset(self):
        queryset = super().get_queryset()
        tag = self.request.query_params.get('tag')
        
        if tag:
            queryset = queryset.filter(tags__icontains=tag)  # 태그 필터링
        return queryset
    
    def perform_create(self, serializer):
        post = serializer.save(author=self.request.user)
        images = self.request.FILES.getlist('images')  # 여러 이미지 업로드 지원
        for image in images:
            PostImage.objects.create(post=post, image=image)

# 좋아요 API
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def like_post(request, post_id):
    post = generics.get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)

    if created:
        return Response({"message": "게시글에 좋아요를 눌렀습니다."}, status=201)
    else:
        like.delete()
        return Response({"message": "게시글 좋아요를 취소했습니다."}, status=200)
    ###
#댓글 좋아요 API
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def like_comment(request, comment_id):
    comment = generics.get_object_or_404(Comment, id=comment_id)
    like, created = Like.objects.get_or_create(user=request.user, comment=comment)

    if created:
        return Response({"message : 댓글에 좋아요를 눌렀습니다."}, status=201)
    else:
        like.delete()
        return Response({"message": "댓글 좋아요를 취소했습니다."}, status=200)
    
# 사용자가 좋아요한 게시글 목록
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def liked_posts(request):
    posts = Post.objects.filter(liked_by__user=request.user)
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)

#사용자가 좋아요한 댓글 목록
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def liked_comments(request):
    comments = Comment.objects.filter(liked_by__user=request.user)
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)
    
# 게시글 북마크 API
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def bookmark_post(request, post_id):
    post = generics.get_object_or_404(Post, id=post_id)
    bookmark, created = Bookmark.objects.get_or_create(user=request.user, post=post)

    if created:
        return Response({"message": "게시글을 북마크했습니다."}, status=201)
    else:
        bookmark.delete()
        return Response({"message": "게시글 북마크를 취소했습니다."}, status=200)
    
# 사용자가 북마크한 게시글 목록
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def bookmarked_posts(request):
    posts = Post.objects.filter(bookmarked_by__user=request.user)
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)

#게시글 상세 조회, 수정, 삭제
class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.prefetch_related('comments').all() #댓글도 함께 불러오기
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        if self.request.user == serializer.instance.author:
            serializer.save()
        else:
            raise PermissionDenied("게시글을 수정할 수 없습니다")

    def perform_destroy(self, instance):
        if self.request.user == instance.author:
            instance.delete()
        else:
            raise PermissionDenied("게시글을 삭제할 수 없습니다")
        
# 특정 사용자가 작성한 게시글 목록
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def user_posts(request, user_id):
    user = generics.get_object_or_404(User, id=user_id)
    posts = Post.objects.filter(author=user).order_by('-created_at')
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)

# 댓글 목록 조회 및 작성
@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly])
def comment_list_create(request, post_id):
    post = generics.get_object_or_404(Post, id=post_id)

    if request.method == 'GET':
        comments = post.comments.all().order_by('created_at')  # 오래된 댓글부터 조회
        serializer = CommentSerializer(comments, many=True, context={"request": request,}) # request 추가
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CommentSerializer(data=request.data,context={"request": request, "post_id": post_id}) #request 추가
        if serializer.is_valid():
            serializer.save(post=post, author=request.user)  # 현재 로그인한 유저가 작성자
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    
# 댓글 삭제
@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def comment_delete(request, comment_id):
    comment = generics.get_object_or_404(Comment, id=comment_id)

    if request.user == comment.author:
        comment.delete()
        return Response({"message": "댓글이 삭제되었습니다."}, status=200)
    else:
        raise PermissionDenied("댓글을 삭제할 수 없습니다.")
    
# 여러 개의 이미지 삭제 API
@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def delete_multiple_post_images(request, post_id):
    post = generics.get_object_or_404(Post, id=post_id)

    # 게시글 작성자만 이미지 삭제 가능
    if request.user != post.author:
        raise PermissionDenied("게시글의 이미지를 삭제할 수 없습니다.")

    image_ids = request.data.get('image_ids', [])  # 삭제할 이미지 ID 리스트 받기

    if not image_ids:
        return Response({"error": "삭제할 이미지 ID 목록을 제공해야 합니다."}, status=400)

    images_to_delete = PostImage.objects.filter(id__in=image_ids, post=post)

    if images_to_delete.exists():
        images_to_delete.delete()
        return Response({"message": "선택한 이미지가 삭제되었습니다."}, status=200)
    else:
        return Response({"error": "해당 이미지가 존재하지 않거나 삭제할 수 없습니다."}, status=404)
    

#마이페이지 (글,댓글,게시글좋아요,댓글좋아요,북마크,내프로필정보)
@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def my_posts(request):
    print(f"현재 로그인한 사용자: {request.user}")  # 디버깅용
    posts = Post.objects.filter(author=request.user).order_by('-created_at')
    serializer = PostSerializer(posts, many=True)
    return Response({
        "user": request.user.username,  # 현재 사용자 정보 추가
        "posts": serializer.data  # 게시글 데이터
    })

@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def my_comments(request):
    comments = Comment.objects.filter(author=request.user).order_by('-created_at')
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)

@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def my_liked_posts(request):
    liked_posts = Post.objects.filter(likes__user=request.user).order_by('-created_at')
    serializer = PostSerializer(liked_posts, many=True)
    return Response(serializer.data)

@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def my_liked_comments(request):
    liked_comments = Comment.objects.filter(likes__user=request.user).order_by('-created_at')
    serializer = CommentSerializer(liked_comments, many=True)
    return Response(serializer.data)

@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def my_bookmarked_posts(request):
    bookmarked_posts = Post.objects.filter(bookmarks__user=request.user).order_by('-created_at')
    serializer = PostSerializer(bookmarked_posts, many=True)
    return Response(serializer.data)

@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def my_profile(request):
    user = request.user
    return Response({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "profile_image": user.profile_image.url if user.profile_image else None,
    })