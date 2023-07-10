from rest_framework import serializers
from .models import Field, News

from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'username')


# 분야
class FieldSerializer(serializers.ModelSerializer):

    class Meta:
        model = Field
        fields = ('pk', 'subject')

# 뉴스 리스트
class NewsListSerializer(serializers.ModelSerializer):

    field = FieldSerializer(read_only = True)
    helpful_count = serializers.IntegerField()
    unhelpful_count = serializers.IntegerField()

    class Meta:
        model = News
        fields =('pk', 'field', 'isflash', 'title', 'content', 'origin_link', 'origin_create_at', 'helpful_count', 'unhelpful_count')


# 뉴스
class NewsSerializer(serializers.ModelSerializer):
    
    field = FieldSerializer(read_only = True)
    views = serializers.IntegerField(read_only=True)
    helpful_users = UserSerializer(read_only=True, many=True)
    unhelpful_users = UserSerializer(read_only=True, many=True)

    class Meta:
        model = News
        fields = ('pk', 'field', 'isflash', 'title', 'content', 'origin_link', 'origin_create_at', 'origin_journal', 'origin_journalist', 'helpful_users', 'unhelpful_users', 'views', )