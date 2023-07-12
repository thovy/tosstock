import asyncio
import random

from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status

from news.models import News, Analyze
from news.serializers import NewsSerializer

def get_score(news_pk):
    score = random.randrange(-5, 6)
    target_news = get_object_or_404(News, pk=news_pk)
    target_analyze = Analyze.objects.create(score=score, news=target_news)
    serializer = NewsSerializer(instance=target_news, data=target_news)
    if serializer.is_valid(raise_exception=True):
        serializer.save(analyze=target_analyze)
        return Response(status=status.HTTP_204_NO_CONTENT)

def create_analyze(news_pk_list):
    for news_pk in news_pk_list:
        get_score(news_pk)
