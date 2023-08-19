import aiohttp
import asyncio
import re
import random
from rest_framework.response import Response
from rest_framework import status
from asgiref.sync import sync_to_async

from bs4 import BeautifulSoup
from django.shortcuts import get_object_or_404

from news.serializers import NewsSerializer, AnalyzeSerializer
from news.models import News, Field
from news import analyzer

import time

NAVER_API_NEWS = "https://openapi.naver.com/v1/search/news"

async def fetch(session, url, headers):
    async with session.get(url, headers=headers) as response:
        if response.status == 200:
            result = await response.json()
            # print('result', result)
            # print('items: ', len(result['items']))
            return result['items']
        else:
            return response.status

async def fetch_detail(session, url):
    async with session.get(url) as response:
        return await response.text()
    

def unit_url(keyword, start):
    return {
        "url": f"{NAVER_API_NEWS}?query={keyword}&display=10&start={start}",
        "headers": {
            "X-Naver-Client-Id": "",
            "X-Naver-Client-Secret": ""
        },
    }

async def get_news_data(html):
    soup = BeautifulSoup(html, 'html.parser')

    # content = soup.select("div#dic_area")
    content = soup.select("article#dic_area")

    if content == []:
        content = soup.select("#articeBody")
        
    # 기사 텍스트만 가져오기
    # list합치기
    content = ''.join(str(content))

    # html태그제거 및 텍스트 다듬기
    pattern1 = '<[^>]*>'
    content = re.sub(pattern=pattern1, repl='', string=content)
    pattern2 = """[\n\n\n\n\n// flash 오류를 우회하기 위한 함수 추가\nfunction _flash_removeCallback() {}"""
    content = content.replace(pattern2, '')

    # await aget 을 이용해서 field 데이터베이스에서 field 객체를 찾아 가져오는 것을 기다려야함.
    # aget_or_create 를 통해서 우리 field 항목이 없으면, 
    target_field = await Field.objects.aget_or_create(subject=soup.find('em', class_='media_end_categorize_item').string)
    news_date = soup.find('span', class_='_ARTICLE_DATE_TIME').attrs['data-date-time']
    if '속보' in soup.find('h2', class_='media_end_head_headline').get_text():
        isFlash = True
    else:
        isFlash = False
    news_data = {
        'title':soup.find('h2', class_='media_end_head_headline').get_text(),
        'content':content,
        # 'content':soup.select_one('._article_content').string,
        'origin_link':soup.find('a', class_='media_end_head_origin_link')['href'],
        'origin_journal':soup.find('img', class_='media_end_head_top_logo_img')['title'],
        'origin_journalist': '없음' if soup.find('em', class_='media_end_head_journalist_name') is None else soup.find('em', class_='media_end_head_journalist_name').string,
        # ? 2023.07.09. 오후 10:01 라는 형식을 datetime 형식으로 바꿔서 저장해야겠는데?
        # 'create_at':soup.find('span', class_='_ARTICLE_DATE_TIME').string,
        'create_at':news_date,
        # 여기서 바로 저장하지말고, field 를 엮어야하는데?
        # 'field':soup.find('em', class_='media_end_categorize_item').string,
        'field':target_field[0],
        'isflash':isFlash
    }
    return {
        "data": news_data,
        "field":target_field[0]
    }



async def search(keyword, total_page):
    apis = [unit_url(keyword, 1+ (i * 10)) for i in range(total_page)]
    # print(apis)

    async with aiohttp.ClientSession() as session:
        all_data = await asyncio.gather(
            *[
                fetch(session, api["url"], api["headers"])
                for api in apis
            ]
        )
        # print('all_data', all_data)
        link_list = []
        for data in all_data:
            if data is not None:
                for item in data:
                    # naver 에 제공되어야 content 를 긁어오기 쉬움.
                    # 106 연예기사 제외(html의 양식이 다름)
                    if item['link'].startswith('https://n.news.naver.com/mnews/article/') and not item['link'].endswith('sid=106'):
                        link_list.append(item['link'])
        # print(link_list)

        # html 파일 가져오기 fetch
        
        # for await 와 asyncio.gather 를 이용한 것이 같을까?
        # for 시간 - 0.24491524696350098
        # gather 시간 - 0.06280994415283203

        # for 문을 이용한 html 가져오기
        # for_start = time.time()
        # all_news_html_by_for = []
        # for url in link_list:
        #     all_news_html_by_for.append(await fetch_detail(session, url))
        # for_end = time.time()

        # asyncio.gather 를 이용한 html 가져오기
        # gather_start = time.time()
        # print('link_list', link_list)
        all_news_html = await asyncio.gather(
            *[fetch_detail(session, url) for url in link_list]
        )
        # gather_end = time.time()

        # print('for', for_end - for_start)
        # print('gather', gather_end - gather_start)

        # html 파일을 parsing 해서 content 정리 후 News model 에 맞도록
        try:
            news_data_list = await asyncio.gather(
                *[get_news_data(news_html) for news_html in all_news_html]
            )
            return news_data_list
        
        except Exception as e:
            print('Error', e)
            return None

def save_data(data_list):
    result_list = []
    for data in data_list:
        # print("data ",data['data'])
        serializer = NewsSerializer(data = data['data'])
        if serializer.is_valid(raise_exception=True):
            # print(data['field'])
            serializer = serializer.save(field = data['field'])
            # print('done')
            result_list.append(serializer.pk)
    return result_list

def run_crawler(keyword):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop = asyncio.get_event_loop()
    # print(keyword)
    crawling_result = loop.run_until_complete(search(keyword, 2))
    # print(crawling_result)
    # print('crawling done')
    loop.close()
    if crawling_result:
        save_result = save_data(crawling_result)
        result_analyze = analyzer.create_analyze(save_result)
        if result_analyze:
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    else:
        save_result = None
        return None
    # print('result', result[0])