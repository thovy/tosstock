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
            return Response(stauts=status.HTTP_401_UNAUTHORIZED)
        
    if request.method == 'GET':
        return article_detail()
    elif request.method == 'PUT':
        # 여기서 user 를 확인하고 update 함수를 반환하는데 왜 다시 update 에서 확인하나요?
        if request.user == target_article.user:
            return update_article()
    elif request.method == 'DELETE':
        if request.user == target_article.user:
            return delete_article()


