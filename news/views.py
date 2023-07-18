import requests
from datetime import date
from django.shortcuts import get_object_or_404
from django.db.models import Count

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from .models import Field, News, Stock, StockDailyData
from .serializers import FieldSerializer, NewsListSerializer, NewsSerializer, StockSerializer, StockDailyDataSerializer

from news import stockapi

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
def news_by_field(request, subject):
    pass

# 뉴스 디테일
def news_detail(request):
    pass

# 뉴스 도움됐어요
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def helpful_news(request, news_pk):
    target_news = get_object_or_404(News, pk=news_pk)
    user = request.user

    if target_news.helpful_users.filter(pk=user.pk).exists():
        target_news.helpful_users.remove(user)
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        target_news.helpful_users.add(user)
        if target_news.unhelpful_users.filter(pk=user.pk).exists():
            target_news.unhelpful_users.remove(user)
        return Response(status=status.HTTP_204_NO_CONTENT)

# 뉴스 도움안돼요
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unhelpful_news(request, news_pk):
    target_news = get_object_or_404(News, pk=news_pk)
    user = request.user

    if target_news.unhelpful_users.filter(pk=user.pk).exists():
        target_news.unhelpful_users.remove(user)
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        target_news.unhelpful_users.add(user)
        if target_news.helpful_users.filter(pk=user.pk).exists():
            target_news.helpful_users.remove(user)
        return Response(status=status.HTTP_204_NO_CONTENT)

# 뉴스 북마크
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def bookmarking_news(request, news_pk):
    target_news = get_object_or_404(News, pk=news_pk)
    user = request.user

    if target_news.bookmark_users.filter(pk=user.pk).exists():
        target_news.bookmark_users.remove(user)
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        target_news.bookmark_users.add(user)
        return Response(status=status.HTTP_204_NO_CONTENT)


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


@api_view(['GET'])
def create_stock(request):
    url = 'http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd'
    payload = {
        "bld": "dbms/MDC/STAT/standard/MDCSTAT01901",
        "locale": "ko_KR",
        "mktId": "STK",
        "share": "1",
        "csvxls_isNo": "false",
    }
    response = requests.post(url, data=payload)
    parsed_response = response.json()['OutBlock_1']
    try:
        for data in parsed_response:
            if data['MKT_TP_NM'] == "KOSPI":
                stock_data = {
                    "stock_code": data['ISU_SRT_CD'],
                    "companyname": data['ISU_ABBRV'],
                }
                # get_or_create 를 최초로 실행하면 다음 data 를 받을 때 매우 빠른 속도로 저장됨.
                stock_data = Stock.objects.get_or_create(stock_code=stock_data['stock_code'], companyname=stock_data['companyname'])
                # get_or_create 를 하면 save 가 필요가 없네?
                # serializer = StockSerializer(data = stock_data)
                # if serializer.is_valid(raise_exception=True):
                #     serializer.save()

                # list(json) 반환함.
                stock_price_data_json = stockapi.daily_stock_data(stock_data['stock_code'])
                # 바로 stock 에 넣는게 좋은 건가 싶긴 한데 try
                stockapi.save_daily_data(stock_data, stock_price_data_json)


        return Response(status=status.HTTP_201_CREATED)
    except Exception as e:
        print("Error : ", e)
        return e
    

@api_view(['GET'])
def create_stock_daily_data(request):
    pass

@api_view(['GET'])
def analyze_news(request, news_pk):
    pass


@api_view(["GET"])
def get_stock_list(request):
    all_stock_list = Stock.objects.annotate().order_by()
    serializer = StockSerializer(all_stock_list, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_stock_daily_data(request):
    response = stockapi.daily_stock_data('005930')
    stock_data = Stock.objects.get(stock_code='005930')
    stockapi.save_daily_data(stock_data, response)
    # response = daily_stock_data(stock_data['stock_code'])
    return response

# 주식 종목 즐겨찾기
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def favorite_stock(request, stock_pk):
    target_stock = get_object_or_404(Stock, pk=stock_pk)
    user = request.user

    if target_stock.favorite_users.filter(pk=user.pk).exists():
        target_stock.favorite_users.remove(user)
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        target_stock.favorite_users.add(user)
        return Response(status=status.HTTP_204_NO_CONTENT)