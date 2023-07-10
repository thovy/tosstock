import requests
from datetime import date
from django.shortcuts import get_object_or_404
from django.db.models import Count

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status

from .models import Field, News, Stock, StockDailyData
from .serializers import FieldSerializer, NewsListSerializer, NewsSerializer, StockSerializer, StockDailyDataSerializer

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


# kis api 를 이용해 stock daily data 가져오기
kisAppKey = "PSBmrTwbZaXtBDIDpGpfjriClmWMlFTvPNNz"
kisAppSecret = "+o0U5S+5qcuY10pdcvtD4sk86+kznBuzZJ+T1Q3R0soSygt/ZYWF7EZW1BTHhlUUlg4bzDsnW3gZgbSiCtauYmQOwDix3J3DqTQ6Zk+bU/3nis3Rnpwxdv7dH5tLXaH7U3T3C07yTt88Dq+nUDGd6JnbMFkjxKkPtUPEvny7rtAmCh+629M="

def get_token():
    url = 'https://openapivts.koreainvestment.com:29443/oauth2/tokenP'
    body = {
      "grant_type": "client_credentials",
      "appkey":kisAppKey,
      "appsecret":kisAppSecret
    }
    response = requests.post(url, json=body)
    # print("token response",response.json())
    return response.json()['access_token']

def daily_stock_data(stock_code):
    token = get_token()
    url = 'https://openapivts.koreainvestment.com:29443/uapi/domestic-stock/v1/quotations/inquire-daily-price'
    payload = {
        "Content-Type":"application/json;charset=UTF-8",
          "authorization":f'Bearer {token}',
          "appkey":kisAppKey,
          "appsecret":kisAppSecret,
          "tr_id":"FHKST01010400",
    }
    params = {
        "FID_COND_MRKT_DIV_CODE":"J",
        "FID_INPUT_ISCD":f'{stock_code}',
        "FID_PERIOD_DIV_CODE":"D",
        "fid_org_adj_prc":"0000000000"
    }
    
    response = requests.post(url, headers=payload, params=params)
    # return Response(response.json()['output'], status=status.HTTP_200_OK)
    return response.json()['output']


# 가져온 daily data 저장
def save_daily_data(stock_data, price_list):
    for data in price_list:
        # print(data['stck_bsop_date'])
        year, month, day = int(data['stck_bsop_date'][:4]), int(data['stck_bsop_date'][4:6]), int(data['stck_bsop_date'][6:])
        bsop_date = date(year, month, day)
        # print("date ",bsop_date)
        
        # 이미 존재하는 daily data 라면 넘기고, 최신꺼부터 찾기 때문에 바로 return 해도 됨.
        if StockDailyData.objects.filter(date=bsop_date).exists():
            return Response(status=status.HTTP_200_OK)
        daily_data = {
            'stock':stock_data,
            'price':data['stck_clpr'],
            'volume':data['acml_vol'],
            'vs':data['prdy_vrss_sign'],
            'date':bsop_date,
        }
        print("daily data ",daily_data)
        serializer = StockDailyDataSerializer(data = daily_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(stock=stock_data)
            # print('done')
    return Response(status=status.HTTP_201_CREATED)



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
                stock_price_data_json = daily_stock_data(stock_data['stock_code'])
                # 바로 stock 에 넣는게 좋은 건가 싶긴 한데 try
                save_daily_data(stock_data, stock_price_data_json)


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

@api_view(['GET'])
def get_stock_daily_data(request):
    response = daily_stock_data('005930')
    stock_data = Stock.objects.get(stock_code='005930')
    save_daily_data(stock_data, response)
    # response = daily_stock_data(stock_data['stock_code'])
    return response