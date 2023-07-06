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
    origin_create_at = models.DateTimeField()

    # 분야, 분야가 null 이라도 기타 분야에 넣으면 되니까.
    field = models.ForeignKey(Field, related_name='news', on_delete=models.SET_NULL, null=True)

    # True:속보, False:일반 / default=False
    isflash = models.BooleanField(default=False)

    helpful_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='helpful_news')
    unhelpful_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='unhelpful_news')
