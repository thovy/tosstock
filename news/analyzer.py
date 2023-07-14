import asyncio
import random

from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status

from news.models import News, Analyze
from news.serializers import NewsSerializer, AnalyzeSerializer

def get_score(news_pk):
    score = random.randrange(-5, 6)
    data = {
        'score':score
    }
    target_news = get_object_or_404(News, pk=news_pk)
    serializer = AnalyzeSerializer(data=data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(news=target_news)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


def create_analyze(news_pk_list):
    for news_pk in news_pk_list:
        get_score(news_pk)
