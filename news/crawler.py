import aiohttp
import asyncio
import time
from bs4 import BeautifulSoup

from rest_framework.response import Response
from rest_framework import status
from .serializers import NewsSerializer
from .models import Field

# 뉴스 생성 - user 가 글을 쓰는 게 아닌, 크롤링으로 등록
# 뉴스 분야 코드 리스트
sections_list = [
    # 정치
    ('100', ['264', '265', '268', '266', '267', '269']),
    # 경제
    ('101', ['259', '258', '261', '771', '260', '262', '310', '263']),
    # 사회
    ('102', ['249', '250', '251', '254', '252', '59b', '255', '256', '276', '257']),
    # 생활/문화
    ('103', ['241', '239', '240', '237', '238', '376', '242', '243', '244', '248', '245']),
    # IT/과학
    ('105', ['731', '226', '227', '230', '732', '283', '229', '228']),
    # 세계
    ('104', ['231', '232', '233', '234', '322'])
]

async def fetch(session, url):
    print('fetch')
    async with session.get(url) as response:
        return await response.text()

async def approach_sections(sections_list):

    print('session')
    async with aiohttp.ClientSession() as session:
        
        url = 'https://news.naver.com/main/list.naver?mode=LS2D&mid=shm&sid1={field}&sid2={subfield}'
        futures = []
        field = sections_list[0][0]
        subfield = sections_list[0][1][0]
        futures.append(asyncio.ensure_future(fetch(session, url.format(field=field, subfield=subfield))))

        # for sections in sections_list:
        #     field = sections[0]
        #     print(field)
        #     for subfield in sections[1]:
        #         print(subfield)
        #         futures.append(asyncio.ensure_future(fetch(session, url.format(field=field, subfield=subfield))))
        #         print(subfield + ' end')
        res = await asyncio.gather(*futures)
        # print(res)
        return res

async def get_link(response_text):
    soup = BeautifulSoup(response_text, 'html.parser')
    links = []
    for item in soup.find_all('ul', class_='type06_headline'):
        for i in item.find_all('dt', class_='photo'):
            link_a = i.find('a')
            link = link_a['href']
            if link.startswith('https://n.news.naver.com/mnews/article/'):
                links.append(link)
    return links


async def get_task_list(session):
    url = 'https://news.naver.com/main/list.naver?mode=LS2D&mid=shm&sid1={field}&sid2={subfield}'
    futures = []
    for sections in sections_list:
        field = sections[0]
        for subfield in sections[1]:
            html = await fetch(session, url.format(field=field, subfield=subfield))
            href = get_link(html)
            # futures.append(asyncio.ensure_future(fetch(session, url.format(field=field, subfield=subfield))))
            futures.append(asyncio.ensure_future(href))
    # 각 분야별 페이지 데이터가 반환될 거고 res 에 차곡차곡 담겨서 반환될거다.
    res = await asyncio.gather(*futures)
    return res

async def get_news_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    news_data = {
        'title':"",
        'content':"",
        'origin_link':"",
        'origin_journal':"",
        'origin_journalist':"",
        'origin_create_at':"",
        'field':"",

    }
    serializer = NewsSerializer(news_data)
    # field = Field()
    # field.subject = '사회'
    # serializer.field = field
    # print(field)
    print(serializer)
    return None

async def get_news_page(session, url_list):
    for url in url_list:
        url = url[0]
        print("url ",url)
        html = await fetch(session, url)
        data = await get_news_data(html)
    return None


async def test():
    limit_time = aiohttp.ClientTimeout(total=60)
    async with aiohttp.ClientSession(timeout=limit_time) as session:
        url_list = await get_task_list(session)
        print("url_list",url_list)
        data_list = await get_news_page(session, url_list)
        return url_list



def run_test():
    print('run test')
    loop = asyncio.new_event_loop()
    print('new', loop)
    asyncio.set_event_loop(loop)
    print('set',loop)
    loop = asyncio.get_event_loop()
    print('get',loop)
    # result = loop.run_until_complete(approach_sections(sections_list))
    result = loop.run_until_complete(test())
    print('end',loop)
    loop.close()
    print('close', loop)
    return Response(result)