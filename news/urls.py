from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('', views.news_all),
    path('subject/<str:subject>/', views.field_news),
    path('<int:news_pk>/', views.news_detail),
    path('<int:news_pk>/helpful/', views.helpful_news),
    path('<int:news_pk>/unhelpful/', views.unhelpful_news),
    path('<int:news_pk>/bookmark/', views.bookmarking_news),
]
