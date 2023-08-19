import asyncio
import aiohttp
import random

from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status

from news.models import News, Analyze
from news.serializers import NewsSerializer, AnalyzeSerializer

from transformers import BertTokenizer, BertForSequenceClassification
import torch

model_name = 'snunlp/KR-FinBert-SC'
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertForSequenceClassification.from_pretrained(model_name)

def analyze_content(news_content):
    inputs = tokenizer.encode_plus(
        news_content, 
        return_tensors='pt', 
        truncation=True, 
        padding=True, 
        max_length=512
    )

    with torch.no_grad():
        outputs = model(**inputs)
    sentiment_label = torch.argmax(outputs.logits).item()
    sentiment_mapping = {0: -1, 1:0, 2:1}
    sentiment = sentiment_mapping[sentiment_label]

    return sentiment


def create_analyze(news_pk_list):
    for news_pk in news_pk_list:
        target_news = get_object_or_404(News, pk=news_pk)
        sentiment = analyze_content(target_news.content)
        # Analyze.objects.create(news=target_news, score=sentiment)
        data = {
            'score': sentiment
        }
        serializer = AnalyzeSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            # print('valid')
            serializer.save(news=target_news)

    return Response(serializer.data, status=status.HTTP_201_CREATED)