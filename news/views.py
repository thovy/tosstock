from django.shortcuts import get_list_or_404
from django.db.models import Count

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from .models import Field, News
from .serializers import FieldSerializer, NewsListSerializer, NewsSerializer

# 뉴스 전체보기
@api_view(['GET'])
def news_all(request):
    all_news = News.objects.annotate(
        helpful_count = Count('helpful_users', distinct=True),
        unhelpful_count = Count('unhelpful_users', distinct=True),
    ).order_by('-pk')

    serializer = NewsListSerializer(all_news, many=True)
    return Response(serializer.data)

# 뉴스 생성 - user 가 글을 쓰는 게 아닌, 크롤링으로 등록
def create_news():
    pass

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