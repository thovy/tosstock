import aiohttp
import asyncio
import time

class HttpClient:
    _session = None

    async def get_session(cls):
        if cls._session is None:
            cls._session = aiohttp.ClientSession()
        return cls._session

# 뉴스 생성 - user 가 글을 쓰는 게 아닌, 크롤링으로 등록
# 뉴스 분야 코드 리스트
sections_list = [
    # 정치
    (100, [264, 265, 268, 266, 267, 269]),
    # 경제
    (101, [259, 258, 261, 771, 260, 262, 310, 263]),
    # 사회
    (102, [249, 250, 251, 254, 252, '59b', 255, 256, 276, 257]),
    # 생활/문화
    (103, [241, 239, 240, 237, 238, 376, 242, 243, 244, 248, 245]),
    # IT/과학
    (105, [731, 226, 227, 230, 732, 283, 229, 228]),
    # 세계
    (104, [231, 232, 233, 234, 322])
]

async def approach_sections(sections_list):
    field = sections_list[0]
    subfield_list = sections_list[1]
    print(field, subfield_list)
    session = await HttpClient.get_session()
    print(session)
    async with session.get('https://google.com') as response:
        content = await response.text()
        print(content)
    return content

async def run_test():
    for sections in sections_list:
        await approach_sections(sections)