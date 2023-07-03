from django.contrib.auth import get_user_model

from rest_framework import serializers
from .models import Article, Comment

User = get_user_model()

class CommentSerializer(serializers.ModelSerializer):

    # 왜 userserializer 를 계속해서 만들어주는가?
    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ('pk', 'username')
            
    user = UserSerializer(read_only = True)

    class Meta:
        model = Comment
        fields = ('pk', 'user', 'content', 'article',)
        read_only_fields = ('article', )

class ArticleListSerializer(serializers.ModelSerializer):

    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ('pk', 'username')
    
    user = UserSerializer(read_only=True)
    comments_count = serializers.IntegerField()
    helpful_count = serializers.IntegerField()
    unhelpful_count = serializers.IntegerField()

    class meta:
        model = Article
        fields = ('pk', 'title', 'created_at', 'views', 'comments_count', 'helpful_count', 'unhelpful_count')

class ArticleSerializer(serializers.ModelSerializer):

    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ('pk', 'username')

    comments = CommentSerializer(many=True, read_only=True)
    user = UserSerializer(read_only=True)
    helpful_users = UserSerializer(read_only=True, many=True)
    unhelpful_users = UserSerializer(read_only=True, many=True)

    class Meta:
        model = Article
        fields = ('pk', 'user', 'title', 'content', 'views', 'comments', 'helpful_users', 'unhelpful_users')
