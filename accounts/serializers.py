from rest_framework import serializers
from django.contrib.auth import get_user_model
from boards.models import Article, Comment

class UserSerializer(serializers.ModelSerializer):

    class ArticleSerializer(serializers.ModelSerializer):

        class Meta:
            model = Article
            fields = ('pk', 'title', 'content', 'views')

    class CommentSerializer(serializers.ModelSerializer):

        class Meta:
            model = Comment
            fields = ('pk', 'content', )
    
    helpful_articles = ArticleSerializer(many=True)
    unhelpful_articles = ArticleSerializer(many=True)
    articles = ArticleSerializer(many=True)
    comments = CommentSerializer(many=True)

    class Meta:
        model = get_user_model()
        fields = ('pk', 'username', 'email', 'isInfluencer', 'helpful_articles', 'unhelpful_articles', 'articles', 'comments', )
