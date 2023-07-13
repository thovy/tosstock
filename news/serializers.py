from rest_framework import serializers
from .models import Field, News, Stock, StockDailyData, Analyze

from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'username',)


# 분야
class FieldSerializer(serializers.ModelSerializer):

    class Meta:
        model = Field
        fields = ('pk', 'subject',)


class AnalyzeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Analyze
        fields = ('pk', 'score', 'news',)
        read_only_fields = ('news',)

# 뉴스 리스트
class NewsListSerializer(serializers.ModelSerializer):

    field = FieldSerializer(read_only = True)
    analyze = AnalyzeSerializer(read_only=True)
    helpful_count = serializers.IntegerField()
    unhelpful_count = serializers.IntegerField()

    class Meta:
        model = News
        fields =('pk', 'field', 'isflash', 'title', 'content', 'origin_link', 'create_at', 'helpful_count', 'unhelpful_count', 'analyze',)


# 뉴스
class NewsSerializer(serializers.ModelSerializer):
    
    field = FieldSerializer(read_only = True)
    analyze = AnalyzeSerializer(read_only=True)
    views = serializers.IntegerField(read_only=True)
    helpful_users = UserSerializer(read_only=True, many=True)
    unhelpful_users = UserSerializer(read_only=True, many=True)

    class Meta:
        model = News
        fields = ('pk', 'field', 'isflash', 'title', 'content', 'origin_link', 'create_at', 'origin_journal', 'origin_journalist', 'helpful_users', 'unhelpful_users', 'views', 'analyze',)

# stock daily data
class StockDailyDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = StockDailyData
        fields = ('pk', 'stock', 'price', 'volume', 'vs', 'date', )
        read_only_fields = ('stock',)

# stock
class StockSerializer(serializers.ModelSerializer):

    stock_daily_data = StockDailyDataSerializer(many=True, read_only=True)

    class Meta:
        model = Stock
        fields = ('pk', 'stock_code', 'companyname', 'stock_daily_data')
