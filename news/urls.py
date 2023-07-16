from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('', views.news_all),
    path('subject/<str:subject>/', views.news_by_field),
    path('crawler/<str:keyword>/', views.create_news),
    # path('field/create/', views.create_field),
    path('stockdata/', views.create_stock),
    path('stockdata/dailydata/', views.get_stock_daily_data),
    path('stock/<int:stock_pk>/favorite/', views.favorite_stock),
    path('<int:news_pk>/', views.news_detail),
    path('<int:news_pk>/helpful/', views.helpful_news),
    path('<int:news_pk>/unhelpful/', views.unhelpful_news),
    path('<int:news_pk>/bookmark/', views.bookmarking_news),
]
