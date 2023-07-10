from django.shortcuts import get_list_or_404
from django.db.models import Count

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status

from .models import Field, News
from .serializers import FieldSerializer, NewsListSerializer, NewsSerializer

# 뉴스 전체보기
# 로그인 유무와 상관없이 모두에게 보여줘야함.
@api_view(['GET'])
def news_all(request):
    all_news = News.objects.annotate(
        helpful_count = Count('helpful_users', distinct=True),
        unhelpful_count = Count('unhelpful_users', distinct=True),
    ).order_by('-pk')

    serializer = NewsListSerializer(all_news, many=True)
    return Response(serializer.data)

# 분야별 뉴스 리스트
def field_news(request, subject):
    pass

# 뉴스 디테일
def news_detail(request):
    pass

# 뉴스 도움됐어요
def helpful_news(request):
    pass

# 뉴스 도움안돼요
def unhelpful_news(request):
    pass

# 뉴스 북마크
def bookmarking_news(request):
    pass



@api_view(['GET'])
def create_news(request, keyword):
    # from .crawler import run_test
    from .naver_api import run_crawler
    result = run_crawler(keyword)
    return Response(status=status.HTTP_201_CREATED)

# aget_or_create 로 만들어주면 필요가 없음.
# @api_view(['POST'])
# def create_field(request):
#     serializer = FieldSerializer(data=request.data)
#     if serializer.is_valid(raise_exception=True):
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
    