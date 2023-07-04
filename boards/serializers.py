from django.contrib.auth import get_user_model

from rest_framework import serializers
from .models import Article, Comment

User = get_user_model()

class CommentSerializer(serializers.ModelSerializer):

    # 왜 userserializer 를 계속해서 만들어주는가?
    # UserSerializer 를 import 해서 사용하면 UserSerializer 에서 ArticleSerializer 를 사용할 때
    # 순환참조가 발생한다.
    # 근데 굳이 이렇게 계속 만들어줄 필요가?
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
    comment_count = serializers.IntegerField()
    helpful_count = serializers.IntegerField()
    unhelpful_count = serializers.IntegerField()

    class Meta:
        model = Article
        fields = ('pk', 'title', 'created_at', 'views', 'comment_count', 'helpful_count', 'unhelpful_count', 'user')


# detail, create, upodate
class ArticleSerializer(serializers.ModelSerializer):

    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ('pk', 'username')

    user = UserSerializer(read_only=True)
    # Validation
    title = serializers.CharField(min_length=2)

    # 조회시 보여줄 영역(read_only=True)
    views = serializers.IntegerField(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    helpful_users = UserSerializer(read_only=True, many=True)
    unhelpful_users = UserSerializer(read_only=True, many=True)

    class Meta:
        model = Article
        fields = ('pk', 'user', 'title', 'content', 'views', 'comments', 'helpful_users', 'unhelpful_users')
