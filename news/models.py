from django.db import models

from django.conf import settings

# 분야(ex.바이오, 전자, 금융, .. )
class Field(models.Model):
    subject = models.CharField(max_length=20)


# News
class News(models.Model):
    title = models.CharField(max_length=100)
    # 속보의 경우엔 content 가 없을 수도?
    content = models.TextField()
    origin_link = models.CharField(max_length=200)
    origin_journal = models.CharField(max_length=50)
    origin_journalist = models.CharField(max_length=50)
    views = models.IntegerField(default=0)

    # 생성만 할까 수정도 할까
    create_at = models.DateTimeField()

    # 분야, 분야가 null 이라도 기타 분야에 넣으면 되니까.
    field = models.ForeignKey(Field, related_name='news', on_delete=models.SET_NULL, null=True)

    # True:속보, False:일반 / default=False
    isflash = models.BooleanField(default=False)

    helpful_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='helpful_news')
    unhelpful_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='unhelpful_news')

    bookmark_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='bookmark_news')

# stock
class Stock(models.Model):
    # 주식 고유 코드 6자리(ISU_SRT_CD)
    stock_code = models.CharField(max_length=6)
    # 회사 이름(ISU_ABBRV)
    companyname = models.CharField(max_length=50)

# stock daily data
class StockDailyData(models.Model):
    # 가격
    price = models.FloatField()
    # 거래량
    volume = models.IntegerField()
    # 전일대비등락
    vs = models.IntegerField()
    # 기준날짜
    date = models.DateField()

    # stock id
    stock = models.ForeignKey(Stock, related_name='stock_daily_data', on_delete=models.CASCADE)


# 분석 데이터
class Analyze(models.Model):
    # 점수 (-5 ~ 5)
    score = models.IntegerField(default=0)

    # 분석한 뉴스
    news = models.ForeignKey(News, related_name='analyze', on_delete=models.CASCADE)
