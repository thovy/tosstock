from django.db import models

from django.conf import settings

class Article(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.IntegerField()

    # user 가 탈퇴해도 게시글은 남아있도록하려면 CASCADE만 빼면 되나?
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='articles', on_delete=models.CASCADE)

    helpful_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='helpful_articles')
    unhelpful_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='unhelpful_articles')


class Comment(models.Model):
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='comments', on_delete=models.CASCADE)
    article = models.ForeignKey(Article, related_name='comments', on_delete=models.CASCADE)

    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_comments')
    unlike_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='unlike_comments')