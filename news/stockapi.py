import requests
from datetime import date

from rest_framework.response import Response
from rest_framework import status

from .models import StockDailyData
from .serializers import StockDailyDataSerializer

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