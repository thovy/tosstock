from rest_framework import serializers
from django.contrib.auth import get_user_model
from boards.models import Article

class ProfileSerializer(serializers.ModelSerializer):

    class ArticleSerializer(serializers.ModelSerializer):

        class Meta:
            model = Article
            fields = ('pk', 'title', 'content', 'views')
    
    helpful_articles = ArticleSerializer(many=True)
    unhelpful_articles = ArticleSerializer(many=True)
    articles = ArticleSerializer(many=True)

    class Meta:
        model = get_user_model()
        fields = ('pk', 'username', 'email', 'helpful_articles', 'unhelpful_articles', 'articles',)
