from django.db import models

from django.conf import settings

class Article(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.IntegerField(default=0)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='articles', on_delete=models.SET_NULL, null=True)

    helpful_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='helpful_articles')
    unhelpful_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='unhelpful_articles')

    bookmark_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='bookmark_articles')


class Comment(models.Model):
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # user 가 삭제되어도 comment 가 삭제되지 않도록
    # SET_NULL 을 이용해 user 가 삭제되면 null 을 넣도록했는데,
    # user 가 null 이어도 문제가 없나?
    # - null 이면 문제가 생기기 때문에 Set Default 혹은 Set 을 이용하도록 합시다.
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='comments', on_delete=models.SET_NULL, null=True)
    # article이 삭제되면 comment도 삭제되도록 cascade
    article = models.ForeignKey(Article, related_name='comments', on_delete=models.CASCADE)

    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_comments')
    dislike_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='dislike_comments')