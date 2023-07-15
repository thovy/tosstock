from rest_framework import serializers
from django.contrib.auth import get_user_model
from boards.models import Article, Comment
from news.models import News

class UserSerializer(serializers.ModelSerializer):

    class ArticleSerializer(serializers.ModelSerializer):

        class Meta:
            model = Article
            fields = ('pk', 'title', 'content', 'views')

    class CommentSerializer(serializers.ModelSerializer):

        class Meta:
            model = Comment
            fields = ('pk', 'content', )
    
    class NewsSerializer(serializers.ModelSerializer):

        class Meta:
            model = News
            fields = ('pk', 'title', 'isflash', )
    
    helpful_articles = ArticleSerializer(many=True)
    unhelpful_articles = ArticleSerializer(many=True)
    articles = ArticleSerializer(many=True)
    comments = CommentSerializer(many=True)
    bookmark_news = NewsSerializer(many=True)

    class Meta:
        model = get_user_model()
        fields = ('pk', 'username', 'email', 'isInfluencer', 'helpful_articles', 'unhelpful_articles', 'articles', 'comments', 'bookmark_news')
