from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('detail/<str:username>/', views.user_detail),
    path('rankup/', views.user_rankup),
]
