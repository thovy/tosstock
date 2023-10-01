from rest_framework import serializers
from django.contrib.auth import get_user_model
from boards.models import Article, Comment
from news.models import News, Stock
from boards.serializers import ArticleSerializer, CommentSerializer
from news.serializers import NewsSerializer

class UserSerializer(serializers.ModelSerializer):

    # class ArticleSerializer(serializers.ModelSerializer):

    #     class Meta:
    #         model = Article
    #         fields = fields = ('pk', 'field', 'user', 'title', 'content', 'views', 'comments', 'helpful_users', 'unhelpful_users')

    # class CommentSerializer(serializers.ModelSerializer):

    #     class Meta:
    #         model = Comment
    #         fields = ('pk', 'content', )
    
    # class NewsSerializer(serializers.ModelSerializer):

    #     class Meta:
    #         model = News
    #         fields = ('pk', 'title', 'isflash', )

    class StockSerializer(serializers.ModelSerializer):

        class Meta:
            model = Stock
            fields = ('pk', 'stock_code', 'companyname',)
    
    helpful_articles = ArticleSerializer(many=True)
    unhelpful_articles = ArticleSerializer(many=True)
    articles = ArticleSerializer(many=True)
    comments = CommentSerializer(many=True)
    bookmark_news = NewsSerializer(many=True)
    favorite_stock = StockSerializer(many=True)

    class Meta:
        model = get_user_model()
        fields = ('pk', 'username', 'email', 'isInfluencer', 'helpful_articles', 'unhelpful_articles', 'articles', 'comments', 'bookmark_news', 'favorite_stock')
