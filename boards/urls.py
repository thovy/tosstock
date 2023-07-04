from django.urls import path
from . import views

app_name = 'boards'

urlpatterns = [
    path('', views.articles_all_and_create),
    path('<int:article_pk>/', views.article_detail),
]
