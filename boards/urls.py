from django.urls import path
from . import views

app_name = 'boards'

urlpatterns = [
    path('', views.articles_all_and_create),
    path('<int:article_pk>/', views.article_detail),
    path('<int:article_pk>/comment/', views.comment_all_and_create),
    path('<int:article_pk>/comment/<int:comment_pk>/', views.update_or_delete_comment),
]
