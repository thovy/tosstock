from django.urls import path
from . import views

app_name = 'boards'

urlpatterns = [
    path('', views.articles_all),
    path('<int:article_pk>/', views.article_detail),
]
