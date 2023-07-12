from django.shortcuts import get_object_or_404
from django.db.models import Count

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated


from boards.models import Article, Comment
from news.models import Field
from boards.serializers import ArticleListSerializer, ArticleSerializer, CommentSerializer


# article 전체보기, 생성
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def articles_all_and_create(request):
    # all_articles = Article.objects.all()

    # GET 으로 요청이 오면
    # django models 의 count 함수를 이용해서 해당 object 에 있는 column 을 다 세는 건가?

    def article_list():
        all_articles = Article.objects.annotate(
            comment_count = Count('comments', distinct=True),
            helpful_count = Count('helpful_users', distinct=True),
            unhelpful_count = Count('unhelpful_users', distinct=True)
        ).order_by('-pk')

        # list 형태로 반환
        serializer = ArticleListSerializer(all_articles, many=True)
        return Response(serializer.data)
    
    # POST 로 요청이 오면
    def create_article():
        serializer = ArticleSerializer(data=request.data)
        target_field = Field.objects.get(pk=request.data['field'])
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, field=target_field)
            # serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    if request.method == 'GET':
        return article_list()
    elif request.method == 'POST':
        return create_article()


# article 상세보기, 수정, 삭제
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def article_detail(request, article_pk):
    # get object 로 잘 합시다.
    target_article = get_object_or_404(Article, pk=article_pk)

    # detail 표시
    def article_detail():
        serializer = ArticleSerializer(target_article)
        return Response(serializer.data)

    # PUT 으로 오면 update
    # PATCH 는 사용하지 않나요?
    def update_article():
        if request.user == target_article.user:
            # print(request.data)
            serializer = ArticleSerializer(instance=target_article, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    # DELETE 로 오면
    def delete_article():
        if request.user == target_article.user:
            target_article.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
    if request.method == 'GET':
        return article_detail()
    elif request.method == 'PUT':
        return update_article()
    elif request.method == 'DELETE':
        return delete_article()


# comment 생성 - article 에서 전체를 가져오기 때문에 전체보기 GET 은 필요 없음.
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def comment_all_and_create(request, article_pk):
    # 현재 article 반환
    article = get_object_or_404(Article, pk=article_pk)

    # 입력한 comment data serialize
    serializer = CommentSerializer(data = request.data)
    # 확인되면,
    # raise_exception = True,
    # 빈 값일 때 에러페이지가 아니라 에러를 띄웁니다.
    if serializer.is_valid(raise_exception=True):
        # 현재 user 와 현재 article 을 comment 에 담아서 save
        serializer.save(user = request.user, article=article)
        # 해당 article 의 comment 전체를 가져오기.
        all_comments = article.comments.all()
        # 전체 comment 를 다시 serialize 해서 반환
        serializer = CommentSerializer(all_comments, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# 댓글 수성, 삭제
@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def update_or_delete_comment(request, article_pk, comment_pk):
    article = get_object_or_404(Article, pk=article_pk)
    target_comment = get_object_or_404(Comment, pk=comment_pk)

    def update_comment():
        if request.user == target_comment.user:
            serializer = CommentSerializer(instance=target_comment, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                all_comments = article.comments.all()
                serializer = CommentSerializer(all_comments, many=True)
                return Response(serializer.data)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    def delete_comment():
        if request.user == target_comment.user:
            target_comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
    if request.method == 'PUT':
        return update_comment()
    elif request.method == 'DELETE':
        return delete_comment()

# 게시글 도움됐어요 누르기
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def helpful_article(request, article_pk):
    target_article = get_object_or_404(Article, pk=article_pk)
    user = request.user
    # all 함수보다 exist 함수를 이용하는 것이 좋습니다.
    # target_article 의 helpful user 목록에 현재 로그인된 user 의 pk 가 존재하나?(exist)
    if target_article.helpful_users.filter(pk=user.pk).exists():
        # 이미 목록에 있다면(이미 버튼을 누른 상태라면) 제거(remove)
        target_article.helpful_users.remove(user)
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        # exist 하지 않는다면 추가(add)
        target_article.helpful_users.add(user)
        # 동시에 싫어요에 user 가 있다면 싫어요 취소
        if target_article.unhelpful_users.filter(pk=user.pk).exists():
            target_article.unhelpful_users.remove(user)
        return Response(status=status.HTTP_204_NO_CONTENT)

# 게시글 도움안돼요 누르기
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unhelpful_article(request, article_pk):
    target_article = get_object_or_404(Article, pk=article_pk)
    user = request.user

    if target_article.unhelpful_users.filter(pk=user.pk).exists():
        target_article.unhelpful_users.remove(user)
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        target_article.unhelpful_users.add(user)
        if target_article.helpful_users.filter(pk=user.pk).exists():
            target_article.helpful_users.remove(user)
        return Response(status=status.HTTP_204_NO_CONTENT)

# 게시글 북마크 누르기
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def bookmarking_article(request, article_pk):
    target_article = get_object_or_404(Article, pk=article_pk)
    user = request.user

    if target_article.bookmark_users.filter(pk=user.pk).exists():
        target_article.bookmark_users.remove(user)
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        target_article.bookmark_users.add(user)
        return Response(status=status.HTTP_204_NO_CONTENT)


# 댓글 좋아요
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_comment(request, article_pk, comment_pk):
    # target_article = get_object_or_404(Article, pk=article_pk)
    target_comment = get_object_or_404(Comment, pk=comment_pk)
    user = request.user

    if target_comment.like_users.filter(pk=user.pk).exists():
        target_comment.like_users.remove(user)
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        target_comment.like_users.add(user)
        if target_comment.dislike_users.filter(pk=user.pk).exists():
            target_comment.dislike_users.remove(user)
        return Response(status=status.HTTP_204_NO_CONTENT)

# 댓글 싫어요
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def dislike_comment(request, article_pk, comment_pk):
    target_comment = get_object_or_404(Comment, pk=comment_pk)
    user = request.user

    if target_comment.dislike_users.filter(pk=user.pk).exists():
        target_comment.dislike_users.remove(user)
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        target_comment.dislike_users.add(user)
        if target_comment.like_users.filter(pk=user.pk).exists():
            target_comment.like_users.remove(user)
        return Response(status=status.HTTP_204_NO_CONTENT)