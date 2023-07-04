from django.shortcuts import get_object_or_404
from django.db.models import Count

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly


from .models import Article, Comment
from .serializers import ArticleListSerializer, ArticleSerializer, CommentSerializer


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
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
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


# comment 생성(article 에서 전체를 가져오기 때문에 전체보기 GET 은 필요 없음.)
@api_view(['POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
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
    
@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
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