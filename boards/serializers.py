from django.contrib.auth import get_user_model

from rest_framework import serializers
from .models import Article, Comment
from news.models import Field

User = get_user_model()

# UserSerializer 를 import 해서 사용하면 UserSerializer 에서 ArticleSerializer 를 사용할 때
# 순환참조가 발생한다.
# 각 serializer 마다 커스텀을 하려면 다시 넣어줍시다. 지금은 커스텀할 게 없어서 빼놓음.
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'username', 'isInfluencer')

class FieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
        fields = ('pk', 'subject', )
        

class CommentSerializer(serializers.ModelSerializer):

    user = UserSerializer(read_only = True)
    content = serializers.CharField(min_length=2)

    class Meta:
        model = Comment
        fields = ('pk', 'user', 'content', 'article', 'like_users', 'dislike_users', )
        read_only_fields = ('article', )


class ArticleListSerializer(serializers.ModelSerializer):
    
    user = UserSerializer(read_only=True)
    field = FieldSerializer(read_only=True)
    comment_count = serializers.IntegerField()
    helpful_count = serializers.IntegerField()
    unhelpful_count = serializers.IntegerField()

    class Meta:
        model = Article
        fields = ('pk', 'field', 'title', 'created_at', 'views', 'comment_count', 'helpful_count', 'unhelpful_count', 'user')


# detail, create, upodate
class ArticleSerializer(serializers.ModelSerializer):

    user = UserSerializer(read_only=True)
    field = FieldSerializer(read_only=True)
    # Validation
    title = serializers.CharField(min_length=2)
    content = serializers.CharField(min_length=10)

    # 조회시 보여줄 영역(read_only=True)
    views = serializers.IntegerField(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    helpful_users = UserSerializer(read_only=True, many=True)
    unhelpful_users = UserSerializer(read_only=True, many=True)

    class Meta:
        model = Article
        fields = ('pk', 'field', 'user', 'title', 'content', 'views', 'comments', 'helpful_users', 'unhelpful_users')
