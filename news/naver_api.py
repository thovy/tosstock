import aiohttp
import asyncio
from rest_framework.response import Response
from rest_framework import status
from bs4 import BeautifulSoup

from .serializers import NewsSerializer
from .models import News

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
            "X-Naver-Client-Id": "18tpK8zgiIufPReidlV8",
            "X-Naver-Client-Secret": "j26brzgOWo"
        },
    }

async def get_news_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    news_data = {
        'title':soup.find('h2', class_='media_end_head_headline').get_text(),
        'content':soup.select_one('._article_content').string,
        'origin_link':soup.find('a', class_='media_end_head_origin_link')['href'],
        'origin_journal':soup.find('img', class_='media_end_head_top_logo_img')['title'],
        'origin_journalist': '없음' if soup.find('em', class_='media_end_head_journalist_name') is None else soup.find('em', class_='media_end_head_journalist_name').string,
        # ? 2023.07.09. 오후 10:01 라는 형식을 datetime 형식으로 바꿔서 저장해야겠는데?
        'origin_create_at':soup.find('span', class_='_ARTICLE_DATE_TIME').string,
        # 여기서 바로 저장하지말고, field 를 엮어야하는데?
        'field':soup.find('em', class_='media_end_categorize_item').string,
    }
    print(news_data)
    return None



async def search(keyword, total_page):
    apis = [unit_url(keyword, 1+ (i * 10)) for i in range(total_page)]
    print(apis)

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
        print(link_list)

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
        all_news_html = await asyncio.gather(
            *[fetch_detail(session, url) for url in link_list]
        )
        # gather_end = time.time()

        # print('for', for_end - for_start)
        # print('gather', gather_end - gather_start)

        # html 파일을 parsing 해서 content 정리 후 News model 에 맞도록
        for news_html in all_news_html:
            await get_news_data(news_html)

        # await get_news_data(all_news_html[0])

        result = []

        return result

def run_test(keyword):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop = asyncio.get_event_loop()
    print(keyword)
    result = loop.run_until_complete(search(keyword, 2))
    # print('result', result[0])
    loop.close()
    return Response(result)